#!/usr/bin/env python3
"""
Check if the Trade-MCP application modules can be imported correctly
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Checking if Trade-MCP application modules can be imported...")

try:
    # Test importing the main modules
    print("Importing config...")
    from trade_mcp.config import HF_TOKEN
    print("✓ Config imported successfully")
    
    print("Importing reasoner...")
    from trade_mcp.reasoner import Reasoner
    print("✓ Reasoner imported successfully")
    
    print("Importing other modules...")
    from trade_mcp.mcp_server import MCP_SERVER_PORT
    from trade_mcp.bot import TELEGRAM_BOT_TOKEN
    from trade_mcp.webui import WEB_UI_PORT
    print("✓ All modules imported successfully")
    
    print("\n🎉 Application modules are ready!")
    print("The Trade-MCP application should start without issues.")
    print("\nTo start the application, run:")
    print("  .\\start-trade-mcp.ps1")
    
except Exception as e:
    print(f"✗ Error importing modules: {e}")
    import traceback
    traceback.print_exc()