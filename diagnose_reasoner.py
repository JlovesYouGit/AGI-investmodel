#!/usr/bin/env python3
"""
Diagnostic script to check reasoner model loading status
"""

import os
import sys
import asyncio
from pathlib import Path

# Set up environment
os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')

def main():
    print("=== Trade-MCP Reasoner Diagnostic ===")
    
    try:
        from trade_mcp.reasoner import Reasoner
        
        print("1. Creating reasoner instance...")
        reasoner = Reasoner()
        print(f"✅ Reasoner created")
        print(f"   Model state: {reasoner.model}")
        print(f"   Model load failed: {reasoner.model_load_failed}")
        
        print("\n2. Testing model loading...")
        async def load_model():
            await reasoner.load_model()
            return reasoner.model, reasoner.model_load_failed
        
        model, model_load_failed = asyncio.run(load_model())
        
        print(f"✅ Model loading completed")
        print(f"   Model state: {model}")
        print(f"   Model load failed: {model_load_failed}")
        
        if model_load_failed or model is None:
            print("\n❌ Model failed to load properly")
            print("   This explains why you're getting fallback responses")
            return 1
        else:
            print("\n✅ Model loaded successfully!")
            
            print("\n3. Testing analysis...")
            async def test_analysis():
                result = await reasoner.analyze("What do you think about NVDA stock?")
                return result
            
            result = asyncio.run(test_analysis())
            print(f"✅ Analysis completed")
            print(f"   Result: {result}")
            
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during diagnostic: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())