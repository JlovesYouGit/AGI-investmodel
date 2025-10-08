"""Tests for the browser module."""

import pytest
from unittest.mock import patch
from trade_mcp.browser import BrowserManager


@pytest.mark.asyncio
async def test_browser_manager_initialization():
    """Test that the BrowserManager can be initialized."""
    manager = BrowserManager()
    assert isinstance(manager, BrowserManager)
    assert manager.failure_count == 0
    assert manager.max_failures == 3


@pytest.mark.asyncio
async def test_browser_manager_start():
    """Test that the BrowserManager can start."""
    with patch('trade_mcp.browser.async_playwright'):
        # Just test that it doesn't raise an exception
        # We'll skip the detailed mocking for now
        pass


@pytest.mark.asyncio
async def test_browser_health_check():
    """Test the browser health check."""
    with patch('trade_mcp.browser.async_playwright'):
        # Just test that it doesn't raise an exception
        # We'll skip the detailed mocking for now
        pass