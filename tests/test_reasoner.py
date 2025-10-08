"""Tests for the reasoner module."""

import pytest
from trade_mcp.reasoner import Reasoner


@pytest.mark.asyncio
async def test_reasoner_initialization():
    """Test that the Reasoner can be initialized."""
    reasoner = Reasoner()
    assert isinstance(reasoner, Reasoner)


@pytest.mark.asyncio
async def test_reasoner_analyze():
    """Test that the Reasoner can analyze a query."""
    reasoner = Reasoner()
    result = await reasoner.analyze("What's your analysis on AAPL?")
    
    # Check that the result contains the expected elements
    assert "ACTION:" in result
    assert "ENTRY:" in result
    assert "STOP:" in result
    assert "TARGET:" in result
    assert "DURATION:" in result
    assert "CONVICTION:" in result
    assert "SUMMARY:" in result


@pytest.mark.asyncio
async def test_reasoner_format_recommendation():
    """Test that the Reasoner can format recommendations."""
    reasoner = Reasoner()
    data = {
        "action": "BUY",
        "entry": 123.45,
        "stop": 120.00,
        "target": 130.00,
        "duration": "3-5 days",
        "conviction": 93,
        "summary": "Strong bullish momentum with positive insider activity.\nTechnical indicators support upward movement."
    }
    
    result = reasoner._format_recommendation(data)
    assert "ACTION: BUY" in result
    assert "ENTRY:  $123.45" in result
    assert "STOP:   $120.00" in result
    assert "TARGET: $130.00" in result
    assert "DURATION: 3-5 days" in result
    assert "CONVICTION: 93 %" in result