#!/usr/bin/env python3
"""
Start the application with model loading fallback
"""

import os
import sys
from pathlib import Path

# Set up environment
os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')

def main():
    print("=== Trade-MCP with Fallback Mode ===")
    print("Starting application in fallback mode (without AI model)...")
    
    try:
        # Test imports
        from trade_mcp.config import HF_TOKEN, WEBUI_HOST
        from trade_mcp.webui import WebUI
        import asyncio
        import gradio as gr
        
        print("✅ All modules imported successfully")
        
        # Create a simple Web UI without trying to start the full application
        print("\nCreating simple Web UI...")
        
        ui = WebUI()
        
        with gr.Blocks(title="Trade-MCP") as demo:
            gr.Markdown("# Trade-MCP: Autonomous Trading Assistant (Fallback Mode)")
            gr.Markdown("Running in fallback mode - AI model not available")
            gr.Markdown("This is a demonstration interface without AI capabilities.")
            
            with gr.Tab("Information"):
                gr.Markdown("""
                ## Fallback Mode Active
                
                The AI model could not be loaded, so this interface is running in fallback mode.
                
                ### Features in Fallback Mode:
                - Basic UI interface
                - Demonstration of intended functionality
                - Framework for future AI integration
                
                ### To Enable Full AI Features:
                1. Ensure model files are complete
                2. Check system memory requirements (8GB+ RAM recommended)
                3. Try clearing and redownloading the model:
                   `python clear-and-redownload-model.py`
                """)
        
        print("✅ Web UI created")
        print("Starting Web UI on port 7864...")
        print("Web UI will be available at: http://localhost:7864")
        print("Press Ctrl+C to stop")
        
        # Start on a different port
        demo.launch(
            server_name="0.0.0.0",
            server_port=7864,
            share=False,
            prevent_thread_lock=True
        )
        
        # Keep running
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⚠️  Application stopped by user")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())