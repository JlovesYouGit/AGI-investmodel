#!/usr/bin/env python3
"""
Test to verify the application can start
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing application startup...")

try:
    # Test importing the main modules
    from trade_mcp import config
    print("✅ Config module imported successfully")
    
    from trade_mcp import reasoner
    print("✅ Reasoner module imported successfully")
    
    from trade_mcp import bot
    print("✅ Bot module imported successfully")
    
    from trade_mcp import webui
    print("✅ WebUI module imported successfully")
    
    from trade_mcp import mcp_server
    print("✅ MCP Server module imported successfully")
    
    print("\n✅ All modules imported successfully!")
    print("The application should be able to start.")
    
except Exception as e:
    print(f"❌ Error during import: {e}")
    import traceback
    traceback.print_exc()