"""Telegram bot implementation for Trade-MCP."""

import asyncio
import json
import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from .config import TELEGRAM_TOKEN, CHATLOG_FILE, CAPITAL_FILE
from .reasoner import Reasoner
from .audio import process_audio

logger = logging.getLogger(__name__)

# Global telegram status
_telegram_alive = False


def telegram_alive() -> bool:
    """Check if the Telegram bot is alive."""
    return _telegram_alive


async def log_message(update: Update, context) -> None:
    """Log incoming messages to chatlog file."""
    if update.message is None:
        return
    
    message_data = {
        "message_id": update.message.message_id,
        "user_id": update.message.from_user.id,
        "username": update.message.from_user.username,
        "text": update.message.text,
        "timestamp": update.message.date.isoformat(),
        "chat_id": update.message.chat_id
    }
    
    # Append to chatlog file
    with open(CHATLOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(message_data) + "\n")
    
    logger.info(f"Logged message from {update.message.from_user.username}")


async def handle_message(update: Update, context) -> None:
    """Handle incoming messages and trigger reasoning pipeline."""
    global _telegram_alive
    _telegram_alive = True
    
    if update.message is None:
        return
    
    # Log the message first
    await log_message(update, context)
    
    # Only respond in groups and private chats
    if update.effective_chat.type not in ["group", "supergroup", "private"]:
        return
    
    # Check if this is an audio message
    if update.message.audio or update.message.voice:
        await handle_audio_message(update, context)
        return
    
    # Trigger reasoning pipeline
    try:
        reasoner = Reasoner()
        result = await reasoner.analyze(update.message.text)
        
        # Send the formatted result back to the chat
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in reasoning pipeline: {e}")
        await update.message.reply_text("Sorry, I encountered an error while processing your request.")


async def handle_audio_message(update: Update, context) -> None:
    """Handle audio messages."""
    global _telegram_alive
    _telegram_alive = True
    
    if update.message is None:
        return
    
    try:
        # Download the audio file
        if update.message.voice:
            file = await update.message.voice.get_file()
        elif update.message.audio:
            file = await update.message.audio.get_file()
        else:
            return
        
        # Save audio file temporarily
        file_path = f".data/temp_audio_{update.message.message_id}.ogg"
        await file.download_to_drive(file_path)
        
        # Process audio
        result = await process_audio(file_path)
        
        # Generate trading recommendation based on emotion
        reasoner = Reasoner()
        recommendation = await reasoner.analyze(
            f"Audio message with {result['emotion']} emotion (confidence: {result['confidence']:.2f}). "
            f"Transcription: {result['transcription']}"
        )
        
        # Send both emotion analysis and trading recommendation
        response = f"🎵 Audio Analysis:\nEmotion: {result['emotion']} (confidence: {result['confidence']:.2f})\nTranscription: {result['transcription']}\n\n"
        response += recommendation
        
        await update.message.reply_text(response, parse_mode="Markdown")
        
        # Clean up temporary file
        os.remove(file_path)
    except Exception as e:
        logger.error(f"Error processing audio message: {e}")
        await update.message.reply_text("Sorry, I encountered an error while processing your audio message.")


async def capital_command(update: Update, context) -> None:
    """Handle the /capital command."""
    global _telegram_alive
    _telegram_alive = True
    
    if update.message is None:
        return
    
    # Check if capital is already set
    if CAPITAL_FILE.exists():
        with open(CAPITAL_FILE, "r") as f:
            capital_data = json.load(f)
        await update.message.reply_text(
            f"Current capital is set to ${capital_data['amount']}. "
            f"To update, use: /capital <amount>"
        )
        return
    
    # If no arguments provided, ask for capital
    if not context.args:
        await update.message.reply_text(
            "Please provide your trading capital. Example: /capital 5000"
        )
        return
    
    try:
        amount = float(context.args[0])
        capital_data = {
            "amount": amount,
            "currency": "USD",
            "timestamp": update.message.date.isoformat()
        }
        
        # Save capital data
        CAPITAL_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CAPITAL_FILE, "w") as f:
            json.dump(capital_data, f)
        
        await update.message.reply_text(
            f"Capital set to ${amount}. "
            f"I'll use this for position sizing in trading recommendations."
        )
    except ValueError:
        await update.message.reply_text(
            "Invalid amount. Please provide a valid number. Example: /capital 5000"
        )
    except Exception as e:
        logger.error(f"Error setting capital: {e}")
        await update.message.reply_text("Sorry, I encountered an error while setting your capital.")


async def start_command(update: Update, context) -> None:
    """Handle the /start command."""
    global _telegram_alive
    _telegram_alive = True
    
    if update.message is None:
        return
    
    # Check if capital is set
    capital_info = ""
    if CAPITAL_FILE.exists():
        with open(CAPITAL_FILE, "r") as f:
            capital_data = json.load(f)
        capital_info = f"\nCurrent capital: ${capital_data['amount']}"
    else:
        capital_info = "\nPlease set your capital using /capital <amount>"
    
    await update.message.reply_text(
        "Welcome to Trade-MCP! I'm your autonomous trading assistant."
        f"{capital_info}\n\n"
        "Send me a message about a stock to get trading recommendations.\n"
        "You can also send voice messages for emotion-based analysis."
    )


async def run_telegram_bot():
    """Run the Telegram bot."""
    global _telegram_alive
    
    if not TELEGRAM_TOKEN:
        logger.warning("TELEGRAM_TOKEN not set, skipping Telegram bot")
        return
    
    logger.info("Starting Telegram bot")
    
    # Ensure chatlog file exists
    CHATLOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHATLOG_FILE.touch(exist_ok=True)
    
    try:
        # Create the Application
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("capital", capital_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio_message))
        
        # Run the bot
        await application.initialize()
        await application.start()
        logger.info("Telegram bot started")
        _telegram_alive = True  # Set the status to True when bot starts successfully
        
        # Keep the bot running
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"Error starting Telegram bot: {e}")
        _telegram_alive = False
        raise