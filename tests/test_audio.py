"""Tests for the audio module."""

import pytest
from unittest.mock import patch, MagicMock
from trade_mcp.audio import process_audio


@pytest.mark.asyncio
async def test_process_audio():
    """Test processing an audio file."""
    with patch("builtins.open", MagicMock()), \
         patch("trade_mcp.audio._save_result") as mock_save:
        result = await process_audio("test_audio.wav")
        
        assert isinstance(result, dict)
        assert "file_path" in result
        assert "transcription" in result
        assert "emotion" in result
        assert "confidence" in result
        mock_save.assert_called_once()