"""Tests for the bot module."""

import pytest
from unittest.mock import patch, MagicMock
from telegram import Update, Message, User
from trade_mcp.bot import log_message, handle_message, start_command, capital_command


@pytest.fixture
def mock_update():
    """Create a mock Telegram update."""
    update = MagicMock(spec=Update)
    update.message = MagicMock(spec=Message)
    update.message.message_id = 1
    update.message.from_user = MagicMock(spec=User)
    update.message.from_user.id = 12345
    update.message.from_user.username = "testuser"
    update.message.text = "Test message"
    update.message.date.isoformat.return_value = "2025-10-01T10:00:00Z"
    update.message.chat_id = 67890
    update.effective_chat.type = "group"
    return update


@pytest.fixture
def mock_context():
    """Create a mock context."""
    return MagicMock()


@pytest.mark.asyncio
async def test_log_message(mock_update, mock_context):
    """Test that messages are logged correctly."""
    with patch("builtins.open", MagicMock()):
        await log_message(mock_update, mock_context)


@pytest.mark.asyncio
async def test_handle_message(mock_update, mock_context):
    """Test that messages are handled correctly."""
    with patch("builtins.open", MagicMock()), \
         patch("trade_mcp.bot.Reasoner") as mock_reasoner:
        mock_reasoner_instance = MagicMock()
        mock_reasoner_instance.analyze.return_value = "Test recommendation"
        mock_reasoner.return_value = mock_reasoner_instance
        
        await handle_message(mock_update, mock_context)


@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    """Test that the start command works."""
    await start_command(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_capital_command_no_args(mock_update, mock_context):
    """Test that the capital command works with no arguments."""
    mock_context.args = []
    await capital_command(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_capital_command_with_args(mock_update, mock_context):
    """Test that the capital command works with arguments."""
    mock_context.args = ["5000"]
    with patch("builtins.open", MagicMock()):
        await capital_command(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()