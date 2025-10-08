"""Web UI for Trade-MCP using Gradio."""

# ------------------------------------------------------------------
# Windows-11 port-rescue preamble – put this at the top of webui.py
# ------------------------------------------------------------------
import os, socket, psutil, gradio as gr

def _find_free_port(start=9999, max_port=65535):
    """Return the first free TCP port >= start."""
    for port in range(start, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allow quick re-bind
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free TCP ports found.")

def _nuke_gradio_on_port(port):
    """Kill any Python process listening on *port* (helps when Gradio zombie stays alive)."""
    try:
        # Use a simpler approach that doesn't rely on psutil connections
        import subprocess
        try:
            # Try to kill any Python processes that might be using the port
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[4]
                        if pid.isdigit():
                            try:
                                print(f"[WinPortFix] Killing process {pid} on port {port}")
                                subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                            except:
                                pass
        except Exception as e:
            print(f"[WinPortFix] Warning: Could not check for zombie processes: {e}")
    except Exception as e:
        print(f"[WinPortFix] Warning: Process cleanup failed: {e}")
        # Continue anyway - the port finding should still work

# 1. Pick a free port (starts at 9999, walks upward)
FREE_PORT = _find_free_port(start=9999)

# 2. Make sure nothing is squatting on it
_nuke_gradio_on_port(FREE_PORT)

# 3. Feed the port to Gradio via env var (zero code changes elsewhere)
os.environ["GRADIO_SERVER_PORT"] = str(FREE_PORT)

print(f"[WinPortFix] Gradio will bind to port {FREE_PORT}")
# ------------------------------------------------------------------
# End of preamble – the rest of your original webui.py continues...
# ------------------------------------------------------------------

import asyncio
import logging
import json
from typing import Any

import gradio as gr
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .config import WEBUI_HOST, WEBUI_PORT
from .reasoner import Reasoner
from .audio import process_audio, get_audio_history

logger = logging.getLogger(__name__)


class WebUI:
    """Web UI for the Trade-MCP application."""
    def __init__(self) -> None:
        """Initialize the web UI."""
        self.reasoner = Reasoner()

    @staticmethod
    def _normalize_model_response(result: Any) -> str:
        """Normalize various model/JSON formats to a user-friendly string."""
        try:
            # If it's a JSON string, try to parse first
            if isinstance(result, str):
                s = result.strip()
                if (s.startswith("{") and s.endswith("}")) or (s.startswith("[") and s.endswith("]")):
                    try:
                        result = json.loads(s)
                    except Exception:
                        return s  # plain string
                else:
                    return s

            # If it's a dict, attempt common schema patterns
            if isinstance(result, dict):
                # Common direct fields
                for key in ("text", "message", "content", "response", "output"):
                    if key in result and isinstance(result[key], (str, int, float)):
                        return str(result[key])

                # OpenAI chat-style: choices -> [{message: {content}}] or [{text}]
                if "choices" in result and isinstance(result["choices"], list) and result["choices"]:
                    choice = result["choices"][0]
                    if isinstance(choice, dict):
                        if "message" in choice and isinstance(choice["message"], dict):
                            content = choice["message"].get("content")
                            if isinstance(content, (str, int, float)):
                                return str(content)
                        if "text" in choice and isinstance(choice["text"], (str, int, float)):
                            return str(choice["text"])

                # Content as array of blocks (various providers)
                if "content" in result and isinstance(result["content"], list):
                    parts = []
                    for item in result["content"]:
                        if isinstance(item, dict):
                            # Prefer text fields in blocks
                            for k in ("text", "content", "value"):
                                if k in item and isinstance(item[k], (str, int, float)):
                                    parts.append(str(item[k]))
                                    break
                        elif isinstance(item, (str, int, float)):
                            parts.append(str(item))
                    if parts:
                        return "\n".join(parts)

                # Fallback to compact JSON
                return json.dumps(result, ensure_ascii=False)

            # If it's a list, join stringifiable items
            if isinstance(result, list):
                parts = []
                for x in result:
                    if isinstance(x, (str, int, float)):
                        parts.append(str(x))
                    elif isinstance(x, dict):
                        # Try common keys
                        for k in ("text", "content", "message", "value"):
                            if k in x and isinstance(x[k], (str, int, float)):
                                parts.append(str(x[k]))
                                break
                        else:
                            parts.append(json.dumps(x, ensure_ascii=False))
                    else:
                        parts.append(str(x))
                return "\n".join(parts)

            # Fallback for other types
            return str(result)
        except Exception:
            # As a last resort, stringify raw result
            try:
                return str(result)
            except Exception:
                return "Unable to render model response."
    
    async def analyze_stock(self, query: str) -> str:
        """Analyze a stock based on user query."""
        try:
            raw = await asyncio.wait_for(self.reasoner.analyze(query), timeout=30.0)
            # Now raw is a dictionary, so format it
            return self.reasoner._format_recommendation(raw)
        except asyncio.TimeoutError:
            return "Model timeout: the AI is busy. Please try again or shorten your query."
        except Exception as e:
            logger.error(f"Error in stock analysis: {e}")
            return f"Error: {str(e)}"
    
    async def process_audio(self, audio_file: str) -> str:
        """Process an uploaded audio file."""
        try:
            result = await process_audio(audio_file)
            return f"Transcription: {result['transcription']}\nEmotion: {result['emotion']} (confidence: {result['confidence']:.2f})"
        except Exception as e:
            logger.error(f"Error in audio processing: {e}")
            return f"Error: {str(e)}"
    
    def get_live_trades(self) -> str:
        """Get live trades information using MCP tools."""
        try:
            # This would typically fetch from a live trading API
            # For now, we'll show market data for major stocks
            import asyncio
            async def get_market_data():
                reasoner = Reasoner()
                symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
                market_data = []

                for symbol in symbols:
                    try:
                        data = await reasoner._mcp_call("browser_scrape_yahoo", {"symbol": symbol})
                        if data and "error" not in data:
                            market_data.append(f"{symbol}: ${data.get('price', 'N/A')} "
                                             f"({data.get('change_percent', 'N/A')})")
                        else:
                            market_data.append(f"{symbol}: Data unavailable")
                    except Exception as e:
                        market_data.append(f"{symbol}: Error fetching data")

                return "\n".join(market_data)

            return asyncio.run(get_market_data())
        except Exception as e:
            logger.error(f"Error getting live trades: {e}")
            return f"Error fetching live trading data: {str(e)}"
    
    def get_finetune_status(self) -> str:
        """Get fine-tuning status."""
        # Placeholder implementation
        return "Fine-tuning not running. Last run: 2025-10-01 10:00 UTC"
    
    def get_insider_feed(self) -> str:
        """Get insider trading feed using MCP tools."""
        try:
            import asyncio
            async def get_insider_data():
                symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
                all_transactions = []

                for symbol in symbols:
                    try:
                        data = await self.reasoner._mcp_call("browser_scrape_openinsider", {"symbol": symbol})
                        if data and len(data) > 0:
                            # Add symbol to each transaction for context
                            for transaction in data[:3]:  # Get top 3 for each symbol
                                transaction["company_symbol"] = symbol
                                all_transactions.append(transaction)
                    except Exception as e:
                        logger.warning(f"Error fetching insider data for {symbol}: {e}")

                if all_transactions:
                    # Sort by date (most recent first) and format
                    formatted_transactions = []
                    for tx in sorted(all_transactions,
                                   key=lambda x: x.get('transaction_date', ''),
                                   reverse=True)[:10]:  # Show top 10 most recent
                        formatted_transactions.append(
                            f"{tx.get('transaction_date', 'N/A')} | "
                            f"{tx.get('company_symbol', 'N/A')} | "
                            f"{tx.get('insider', 'Unknown')} | "
                            f"{tx.get('transaction_type', 'N/A')} | "
                            f"{tx.get('qty', 'N/A')} shares @ ${tx.get('price', 'N/A')}"
                        )
                    return "Recent insider transactions:\n" + "\n".join(formatted_transactions)
                else:
                    return "No recent insider trading data available"

            return asyncio.run(get_insider_data())
        except Exception as e:
            logger.error(f"Error getting insider feed: {e}")
            return f"Error fetching insider trading data: {str(e)}"


async def get_audio_history_display() -> str:
    """Get formatted audio history for display."""
    try:
        history = await get_audio_history(10)
        if not history:
            return "No audio analysis history available"

        formatted = []
        for item in history:
            formatted.append(
                f"📁 {item.get('file_path', 'Unknown')}\n"
                f"🕐 {item.get('timestamp', 'Unknown')}\n"
                f"😊 Emotion: {item.get('emotion', 'Unknown')} (confidence: {item.get('confidence', 0):.2f})\n"
                f"📝 {item.get('transcription', 'No transcription')[:100]}...\n"
            )

        return "\n" + "="*50 + "\n".join(formatted)
    except Exception as e:
        return f"Error loading audio history: {str(e)}"


async def start_webui() -> None:
    """Start the Gradio web UI."""
    logger.info("Starting Gradio web UI")
    
    ui = WebUI()
    
    with gr.Blocks(title="Trade-MCP") as demo:
        gr.Markdown("# Trade-MCP: Autonomous Trading Assistant")
        gr.Markdown("Get AI-powered trading recommendations and insights.")
        
        with gr.Tab("Chat"):
            with gr.Row():
                with gr.Column():
                    chat_input = gr.Textbox(label="Enter stock symbol or query", lines=3)
                    chat_button = gr.Button("Analyze")
                with gr.Column():
                    chat_output = gr.Markdown(label="Recommendation")
            
            chat_button.click(
                fn=ui.analyze_stock,
                inputs=chat_input,
                outputs=chat_output
            )
        
        with gr.Tab("Audio Analysis"):
            with gr.Row():
                with gr.Column():
                    audio_input = gr.Audio(label="Upload audio file", type="filepath")
                    audio_button = gr.Button("Analyze Emotion")
                with gr.Column():
                    audio_output = gr.Textbox(label="Result", lines=5)
            
            audio_button.click(
                fn=ui.process_audio,
                inputs=audio_input,
                outputs=audio_output
            )
        
        with gr.Tab("Audio History"):
            with gr.Row():
                history_output = gr.Textbox(label="Recent Audio Analyses", lines=10)
                history_button = gr.Button("Refresh History")
            
            history_button.click(
                fn=lambda: asyncio.run(get_audio_history_display()),
                inputs=None,
                outputs=history_output
            )
        
        with gr.Tab("Live Trades"):
            with gr.Row():
                trades_output = gr.Textbox(label="Current Trades", lines=10)
                trades_button = gr.Button("Refresh")
            
            trades_button.click(
                fn=ui.get_live_trades,
                inputs=None,
                outputs=trades_output
            )
        
        with gr.Tab("Fine-tune Status"):
            with gr.Row():
                finetune_output = gr.Textbox(label="Status", lines=10)
                finetune_button = gr.Button("Refresh")
            
            finetune_button.click(
                fn=ui.get_finetune_status,
                inputs=None,
                outputs=finetune_output
            )
        
        with gr.Tab("Insider Feed"):
            with gr.Row():
                insider_output = gr.Textbox(label="Recent Insider Transactions", lines=10)
                insider_button = gr.Button("Refresh")
            
            insider_button.click(
                fn=ui.get_insider_feed,
                inputs=None,
                outputs=insider_output
            )
    
    # Attach a minimal manifest.json route to the underlying FastAPI app via add_api_route
    try:
        fastapi_app = demo.app  # Gradio exposes its FastAPI app
        def _manifest_handler():
            return JSONResponse(content={
                "name": "Trade-MCP",
                "short_name": "Trade-MCP",
                "start_url": "/",
                "display": "standalone",
                "background_color": "#ffffff",
                "theme_color": "#0b5ed7",
                "icons": [
                    {
                        "src": "/favicon.ico",
                        "sizes": "64x64 32x32 24x24 16x16",
                        "type": "image/x-icon"
                    }
                ]
            })
        fastapi_app.add_api_route("/manifest.json", _manifest_handler, methods=["GET"])
    except Exception as e:
        logger.warning(f"Failed to add manifest route: {e}")
    
    # Enable request queue for async handlers (no args for compatibility)
    demo.queue()
    # Start the web server (blocks main thread to keep process alive)
    demo.launch(
        server_name=WEBUI_HOST,
        server_port=FREE_PORT,  # Use the dynamically found free port
        share=False,
        prevent_thread_lock=False,
        quiet=False,  # Show startup messages to see the actual port
        show_api=False,  # Don't show API docs
        inbrowser=False  # Don't try to open browser
    )
    
    logger.info(f"Web UI started at http://{WEBUI_HOST}:{FREE_PORT}")


if __name__ == "__main__":
    asyncio.run(start_webui())
