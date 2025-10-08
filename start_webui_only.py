#!/usr/bin/env python3
"""
Script to start only the Web UI for testing
"""

import os
import sys
import asyncio
from pathlib import Path

def main():
    print("=== Trade-MCP Web UI Only ===")
    print("Starting only the Web UI interface for testing...")
    
    # Set up environment
    os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')
    os.environ['HF_HUB_ENABLE_HF_XET'] = '1'
    
    print(f"Working directory: {os.getcwd()}")
    
    try:
        # Test if we can import the webui module
        print("\n1. Testing Web UI module import...")
        from trade_mcp.webui import start_webui, WebUI
        print("✅ Web UI module imported successfully")
        
        # Test WebUI class instantiation
        print("\n2. Testing Web UI instantiation...")
        ui = WebUI()
        print("✅ Web UI instantiated successfully")
        
        # Start only the Web UI
        print("\n3. Starting Web UI...")
        print("Web UI will be available at: http://localhost:7863")
        print("Press Ctrl+C to stop the Web UI")
        
        # Run the Web UI
        asyncio.run(start_webui())
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Web UI stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting Web UI: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())