"""MCP Server implementation for Trade-MCP."""

import asyncio
import logging
from typing import Any, Dict, List

from mcp.server import FastMCP

from .browser import browser_manager
from .tools import (
    ddg_news_search,
    audio_emotion_tool,
    telegram_history_tool
)

logger = logging.getLogger(__name__)

# Global server status
_server_alive = False


def mcp_server_alive() -> bool:
    """Check if the MCP server is alive."""
    return _server_alive


async def scrape_openinsider(symbol: str) -> List[Dict[str, Any]]:
    """Scrape openinsider.com for insider trading data."""
    try:
        # Check if browser manager is available
        if not hasattr(browser_manager, 'browser') or browser_manager.browser is None:
            logger.warning("Browser manager not initialized, returning empty result")
            return []
            
        page = await browser_manager.get_page()
        await page.goto(f"https://openinsider.com/screener?s={symbol}", wait_until='domcontentloaded')
        
        # Extract table data
        rows = await page.query_selector_all("table.tinytable tr")
        data = []
        
        for row in rows[1:]:  # Skip header
            cells = await row.query_selector_all("td")
            if len(cells) >= 10:
                try:
                    data.append({
                        "transaction_date": await cells[1].inner_text(),
                        "ticker": await cells[2].inner_text(),
                        "company": await cells[3].inner_text(),
                        "insider": await cells[4].inner_text(),
                        "title": await cells[5].inner_text(),
                        "transaction_type": await cells[6].inner_text(),
                        "price": await cells[7].inner_text(),
                        "qty": await cells[8].inner_text(),
                        "value": await cells[9].inner_text(),
                    })
                except Exception as e:
                    # Log the error and continue with the next row
                    logger.warning(f"Error processing row in openinsider scrape: {e}")
                    continue
        
        await page.close()
        return data
    except Exception as e:
        logger.error(f"Error scraping openinsider for {symbol}: {e}")
        return []


async def scrape_yahoo_finance(symbol: str) -> Dict[str, Any]:
    """Scrape finance.yahoo.com for stock data."""
    try:
        # Check if browser manager is available
        if not hasattr(browser_manager, 'browser') or browser_manager.browser is None:
            logger.warning("Browser manager not initialized, returning error result")
            return {"symbol": symbol, "error": "Browser not available"}
            
        page = await browser_manager.get_page()
        await page.goto(f"https://finance.yahoo.com/quote/{symbol}", wait_until='domcontentloaded')
        
        # Extract key data
        data = {
            "symbol": symbol,
            "price": None,
            "change": None,
            "change_percent": None,
            "market_cap": None,
            "volume": None,
            "pe_ratio": None
        }
        
        try:
            # Current price
            price_element = await page.query_selector("[data-field='regularMarketPrice']")
            if price_element:
                data["price"] = await price_element.inner_text()
            
            # Change
            change_element = await page.query_selector("[data-field='regularMarketChange']")
            if change_element:
                data["change"] = await change_element.inner_text()
            
            # Change percent
            change_percent_element = await page.query_selector("[data-field='regularMarketChangePercent']")
            if change_percent_element:
                data["change_percent"] = await change_percent_element.inner_text()
        except Exception as e:
            # Log the error but continue with default values
            logger.warning(f"Failed to extract some Yahoo Finance data: {e}")
        
        await page.close()
        return data
    except Exception as e:
        logger.error(f"Error scraping Yahoo Finance for {symbol}: {e}")
        return {"symbol": symbol, "error": str(e)}


async def handle_tool_call(tool_name: str, args: Dict[str, Any]) -> Any:
    """Dispatch a tool call by name to the appropriate handler.

    Args:
        tool_name: The registered tool name.
        args: Parameters dict passed to the tool.

    Returns:
        The result returned by the tool handler.

    Raises:
        ValueError: If the tool name is unknown.
    """
    if tool_name == "browser_scrape_openinsider":
        return await scrape_openinsider(str(args.get("symbol", "")))
    if tool_name == "browser_scrape_yahoo":
        return await scrape_yahoo_finance(str(args.get("symbol", "")))
    if tool_name == "ddg_news":
        return await ddg_news_search(str(args.get("query", "")))
    if tool_name == "audio_emotion":
        # Support multiple possible keys for file input
        file_path = args.get("file") or args.get("path") or args.get("audio") or ""
        return await audio_emotion_tool(str(file_path))
    if tool_name == "telegram_history":
        # Only limit is supported by the tool signature
        limit_val = args.get("limit", 5)
        try:
            limit = int(limit_val) if limit_val is not None else 5
        except Exception:
            limit = 5
        return await telegram_history_tool(limit)

    raise ValueError(f"Unknown tool: {tool_name}")


async def start_mcp_server() -> None:
    """Start the MCP server."""
    global _server_alive
    logger.info("Starting MCP server")
    
    # Initialize browser manager
    try:
        await browser_manager.start()  # type: ignore[no-untyped-call]
        logger.info("Browser manager initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize browser manager: {e}")
    
    # Create FastMCP server
    server = FastMCP("trade-mcp")
    
    # Register tools using the FastMCP API
    server.add_tool(
        fn=scrape_openinsider,
        name="browser_scrape_openinsider",
        description="Scrape openinsider.com for insider trading data"
    )
    
    server.add_tool(
        fn=scrape_yahoo_finance,
        name="browser_scrape_yahoo",
        description="Scrape finance.yahoo.com for stock data"
    )
    
    server.add_tool(
        fn=ddg_news_search,
        name="ddg_news",
        description="Search news using DuckDuckGo"
    )
    
    server.add_tool(
        fn=audio_emotion_tool,
        name="audio_emotion",
        description="Analyze emotion from audio file"
    )
    
    server.add_tool(
        fn=telegram_history_tool,
        name="telegram_history",
        description="Get Telegram message history"
    )
    
    _server_alive = True
    
    # Start the server
    await server.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(start_mcp_server())