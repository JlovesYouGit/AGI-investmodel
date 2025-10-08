"""Integration tests for Trade-MCP."""

import os
import sys
import json
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from trade_mcp.config import DATA_DIR, CHATLOG_FILE, LORA_DIR, CAPITAL_FILE


def test_data_directories():
    """Test that data directories are created correctly."""
    # Check that data directories exist
    assert DATA_DIR.exists(), f"Data directory {DATA_DIR} does not exist"
    assert DATA_DIR.is_dir(), f"Data directory {DATA_DIR} is not a directory"
    
    # Check that subdirectories exist
    logs_dir = DATA_DIR / "logs"
    assert logs_dir.exists(), f"Logs directory {logs_dir} does not exist"
    assert logs_dir.is_dir(), f"Logs directory {logs_dir} is not a directory"
    
    # Check that LORA directory exists
    assert LORA_DIR.exists(), f"LORA directory {LORA_DIR} does not exist"
    assert LORA_DIR.is_dir(), f"LORA directory {LORA_DIR} is not a directory"
    
    print("✓ Data directories test passed")


def test_config_files():
    """Test that config files are accessible."""
    # Check that chatlog file exists
    assert CHATLOG_FILE.parent.exists(), f"Chatlog directory {CHATLOG_FILE.parent} does not exist"
    
    print("✓ Config files test passed")


def test_capital_file():
    """Test that capital file can be created and read."""
    # Ensure data directory exists
    CAPITAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Create test capital data
    capital_data = {
        "amount": 5000,
        "currency": "USD",
        "timestamp": "2025-10-01T10:00:00Z"
    }
    
    # Write to file
    with open(CAPITAL_FILE, "w") as f:
        json.dump(capital_data, f)
    
    # Read from file
    with open(CAPITAL_FILE, "r") as f:
        loaded_data = json.load(f)
    
    assert loaded_data["amount"] == 5000
    assert loaded_data["currency"] == "USD"
    
    # Clean up
    os.remove(CAPITAL_FILE)
    
    print("✓ Capital file test passed")


if __name__ == "__main__":
    test_data_directories()
    test_config_files()
    test_capital_file()
    print("All integration tests passed!")