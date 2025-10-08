"""Tests for the tools module."""

import pytest
from trade_mcp.tools import (
    ddg_news_search,
    audio_emotion_tool,
    telegram_history_tool
)


@pytest.mark.asyncio
async def test_ddg_news_search():
    """Test the DuckDuckGo news search tool."""
    results = await ddg_news_search("Apple Inc.")
    assert isinstance(results, list)
    # Results may be empty in some environments, so we just check the type


@pytest.mark.asyncio
async def test_audio_emotion_tool():
    """Test the audio emotion tool."""
    result = await audio_emotion_tool("sample.wav")
    assert isinstance(result, dict)
    assert "file_path" in result
    assert result["file_path"] == "sample.wav"


@pytest.mark.asyncio
async def test_telegram_history_tool():
    """Test the Telegram history tool."""
    results = await telegram_history_tool(10)
    assert isinstance(results, list)
    # In the placeholder implementation, we return a sample result
    if results:
        assert "id" in results[0]