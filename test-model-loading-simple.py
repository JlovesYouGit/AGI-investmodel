#!/usr/bin/env python3
"""
Simple test to verify the model can be loaded
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up environment
os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')
os.environ['HF_HUB_ENABLE_HF_XET'] = '1'

print("Testing model loading...")

try:
    from trade_mcp.reasoner import Reasoner
    import asyncio
    
    async def test_model_loading():
        reasoner = Reasoner()
        print("Attempting to load model...")
        await reasoner.load_model()
        print("Model loading completed")
        print(f"Model loaded: {reasoner.model is not None}")
        print(f"Model load failed: {reasoner.model_load_failed}")
        
        if not reasoner.model_load_failed and reasoner.model is not None:
            print("Model loaded successfully!")
            return True
        else:
            print("Model failed to load")
            return False
    
    success = asyncio.run(test_model_loading())
    if success:
        print("\n✅ Model loading test passed!")
    else:
        print("\n❌ Model loading test failed!")
        
except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()