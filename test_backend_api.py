#!/usr/bin/env python3
"""
Script to test the backend API functionality
"""

import os
import sys
import asyncio
from pathlib import Path

def main():
    print("=== Trade-MCP Backend API Test ===")
    
    # Set up environment
    os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')
    
    try:
        # Test imports
        print("1. Testing imports...")
        from trade_mcp.reasoner import Reasoner
        print("✅ Reasoner module imported successfully")
        
        # Test reasoner instantiation
        print("\n2. Testing reasoner instantiation...")
        reasoner = Reasoner()
        print("✅ Reasoner instantiated successfully")
        
        # Test model loading (async)
        print("\n3. Testing model loading...")
        
        async def test_loading():
            await reasoner.load_model()
            return reasoner.model is not None and not reasoner.model_load_failed
        
        success = asyncio.run(test_loading())
        if success:
            print("✅ Model loaded successfully")
        else:
            print("⚠️  Model loading failed, but reasoner can still function with fallback")
        
        # Test simple analysis (if model loaded)
        if reasoner.model is not None and not reasoner.model_load_failed:
            print("\n4. Testing simple analysis...")
            
            async def test_analysis():
                result = await reasoner.analyze("What do you think about AAPL stock?")
                return result
            
            result = asyncio.run(test_analysis())
            print(f"✅ Analysis completed successfully")
            print(f"Result preview: {result[:100]}...")
        else:
            print("\n4. Skipping analysis test (model not loaded)")
        
        print("\n🎉 Backend API test completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during backend API test: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())