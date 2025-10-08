"""Tests for the config module."""

from trade_mcp.config import HF_TOKEN, TELEGRAM_TOKEN


def test_config_defaults():
    """Test that config values have expected defaults."""
    assert HF_TOKEN == "YOUR_HF_TOKEN_HERE"
    assert TELEGRAM_TOKEN == "YOUR_TELEGRAM_TOKEN_HERE"
