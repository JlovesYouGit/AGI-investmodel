#!/usr/bin/env python3
"""
Script to test basic backend functionality without model loading
"""

import os
import sys
from pathlib import Path

def main():
    print("=== Trade-MCP Basic Backend Test ===")
    
    try:
        # Test imports
        print("1. Testing imports...")
        from trade_mcp.config import HF_TOKEN, WEBUI_HOST, WEBUI_PORT
        from trade_mcp.reasoner import Reasoner
        print("✅ Modules imported successfully")
        
        # Test configuration
        print("\n2. Testing configuration...")
        print(f"HF_TOKEN set: {HF_TOKEN is not None}")
        print(f"Web UI Host: {WEBUI_HOST}")
        print(f"Web UI Port: {WEBUI_PORT}")
        
        # Test reasoner instantiation
        print("\n3. Testing reasoner instantiation...")
        reasoner = Reasoner()
        print(f"✅ Reasoner instantiated successfully")
        print(f"Model state: {reasoner.model}")
        print(f"Model load failed: {reasoner.model_load_failed}")
        
        # Test other modules
        print("\n4. Testing other modules...")
        from trade_mcp import bot, webui, mcp_server
        print("✅ All modules imported successfully")
        
        print("\n🎉 Basic backend test completed successfully!")
        print("The backend components are working properly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during basic backend test: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())