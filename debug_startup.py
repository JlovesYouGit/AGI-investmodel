#!/usr/bin/env python3
"""
Simple test script to debug Trade-MCP startup issues
"""

import os
import sys

print("=== Trade-MCP Debug Test ===")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")

try:
    print("\n1. Testing basic imports...")
    # These imports are used for testing, so we'll keep them even if not directly used
    import gradio  # noqa: F401
    print("✓ Gradio imported successfully")

    import fastapi  # noqa: F401
    print("✓ FastAPI imported successfully")

    print("\n2. Testing Google AI import...")
    import google.generativeai as genai
    print("✓ Google Generative AI imported successfully")

    print("\n3. Testing API key...")
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"✓ API key found (length: {len(api_key)})")
        genai.configure(api_key=api_key)
        print("✓ API configured successfully")

        print("\n4. Testing model initialization...")
        try:
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            print("✓ Model initialized successfully")

            print("\n5. Testing basic generation...")
            response = model.generate_content("Hello, test message")
            print(f"✓ Generation test successful: {len(response.text)} characters")
        except Exception as e:
            print(f"✗ Model test failed: {e}")
    else:
        print("✗ No API key found")

    print("\n6. Testing trade_mcp imports...")
    try:
        import trade_mcp.config
        print("✓ trade_mcp.config imported successfully")

        import trade_mcp.reasoner
        print("✓ trade_mcp.reasoner imported successfully")

        import trade_mcp.webui  # noqa: F401
        print("✓ trade_mcp.webui imported successfully")
    except Exception as e:
        print(f"✗ trade_mcp import failed: {e}")

except Exception as e:
    print(f"✗ Error during test: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Debug test completed ===")
input("Press Enter to exit...")