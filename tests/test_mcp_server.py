"""Tests for the MCP server module."""

import pytest
from unittest.mock import patch, MagicMock
from trade_mcp.mcp_server import (
    scrape_openinsider, 
    scrape_yahoo_finance, 
    handle_tool_call,
    mcp_server_alive
)


@pytest.mark.asyncio
async def test_scrape_openinsider():
    """Test scraping openinsider.com."""
    with patch('trade_mcp.mcp_server.browser_manager') as mock_browser:
        mock_page = MagicMock()
        mock_browser.get_page.return_value = mock_page
        mock_page.query_selector_all.return_value = []
        
        result = await scrape_openinsider("AAPL")
        assert isinstance(result, list)


@pytest.mark.asyncio
async def test_scrape_yahoo_finance():
    """Test scraping finance.yahoo.com."""
    with patch('trade_mcp.mcp_server.browser_manager') as mock_browser:
        mock_page = MagicMock()
        mock_browser.get_page.return_value = mock_page
        
        result = await scrape_yahoo_finance("AAPL")
        assert isinstance(result, dict)
        assert "symbol" in result


@pytest.mark.asyncio
async def test_handle_tool_call():
    """Test handling tool calls."""
    with patch('trade_mcp.mcp_server.scrape_openinsider') as mock_scrape_openinsider:
        mock_scrape_openinsider.return_value = []
        
        result = await handle_tool_call("browser_scrape_openinsider", {"symbol": "AAPL"})
        assert result == []


def test_mcp_server_alive():
    """Test the MCP server alive check."""
    # Initially should be False
    assert mcp_server_alive() is False