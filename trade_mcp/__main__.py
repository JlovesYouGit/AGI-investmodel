"""Main entry point for the Trade-MCP application."""

import asyncio
import logging
from pathlib import Path

from .bot import run_telegram_bot
from .browser import browser_manager
from .finetune_worker import finetune_worker
from .health import app as health_app
from .mcp_server import start_mcp_server
from .webui import start_webui

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(".data/logs/app.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def start_health_server():
    """Start the health check server."""
    import uvicorn
    import os
    host = os.getenv("HEALTH_HOST", "127.0.0.1")  # Changed from hardcoded "0.0.0.0" to use environment variable
    config = uvicorn.Config(health_app, host=host, port=8081, log_level="info")  # Changed from 8080 to 8081
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    """Start all components of the Trade-MCP application."""
    logger.info("Starting Trade-MCP application")
    
    # Ensure data directory exists
    Path(".data/logs").mkdir(parents=True, exist_ok=True)
    
    # Start browser manager
    await browser_manager.start()
    
    # Start fine-tune worker
    finetune_worker.start()
    
    # Start all components
    await asyncio.gather(
        start_mcp_server(),
        run_telegram_bot(),
        start_webui(),
        start_health_server()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down Trade-MCP application")
    except SystemExit:
        logger.info("Trade-MCP application terminated by system exit")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        raise SystemExit(1)