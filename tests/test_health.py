"""Tests for the health module."""

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from trade_mcp.health import app


@pytest.fixture
def client():
    """Create a test client for the health app."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_health_check_healthy(client):
    """Test the health check endpoint when healthy."""
    with patch('trade_mcp.health.browser_manager') as mock_browser, \
         patch('trade_mcp.health.telegram_alive') as mock_telegram, \
         patch('trade_mcp.health.mcp_server_alive') as mock_mcp:
        
        # Mock the health check methods to return True
        mock_browser.health_check = AsyncMock(return_value=True)
        mock_telegram.return_value = True
        mock_mcp.return_value = True
        
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "components": {
                "browser": True,
                "telegram": True,
                "mcp_server": True
            }
        }


def test_health_check_unhealthy(client):
    """Test the health check endpoint when unhealthy."""
    with patch('trade_mcp.health.browser_manager') as mock_browser, \
         patch('trade_mcp.health.telegram_alive') as mock_telegram, \
         patch('trade_mcp.health.mcp_server_alive') as mock_mcp:
        
        # Mock the health check methods to return False
        mock_browser.health_check = AsyncMock(return_value=False)
        mock_telegram.return_value = True
        mock_mcp.return_value = True
        
        response = client.get("/healthz")
        assert response.status_code == 503