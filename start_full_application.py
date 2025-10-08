#!/usr/bin/env python3
"""
Script to start the full Trade-MCP application with proper backend and frontend
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    print("=== Trade-MCP Full Application Startup ===")
    print("Starting backend services and frontend interface...")
    
    # Set up environment
    os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')
    os.environ['HF_HUB_ENABLE_HF_XET'] = '1'
    os.environ['TRANSFORMERS_OFFLOAD_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'offload')
    
    print(f"Working directory: {os.getcwd()}")
    print(f"HF_HOME: {os.environ.get('HF_HOME')}")
    
    # Ensure required directories exist
    Path(".data/logs").mkdir(parents=True, exist_ok=True)
    Path("offload").mkdir(parents=True, exist_ok=True)
    
    try:
        # Test if we can import the main modules
        print("\n1. Testing module imports...")
        from trade_mcp import config, reasoner, bot, webui, mcp_server
        print("✅ All modules imported successfully")
        
        # Test model loading
        print("\n2. Testing model loading...")
        import asyncio
        from trade_mcp.reasoner import Reasoner
        
        async def test_model():
            reasoner = Reasoner()
            await reasoner.load_model()
            return not reasoner.model_load_failed
        
        model_success = asyncio.run(test_model())
        if model_success:
            print("✅ Model loaded successfully")
        else:
            print("⚠️  Model loading failed, but application can still start with fallback")
        
        # Start the main application
        print("\n3. Starting main application...")
        print("This will start all services including:")
        print("  - Telegram bot")
        print("  - Web UI (Gradio)")
        print("  - MCP server")
        print("  - Browser services")
        print("\nPress Ctrl+C to stop all services")
        
        # Run the main application module
        subprocess.run([sys.executable, "-m", "trade_mcp"], check=True)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n✅ Trade-MCP application started successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())