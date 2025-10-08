#!/usr/bin/env python3
"""
Script to test if the reasoner can load the model properly
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trade_mcp.reasoner import Reasoner

async def test_reasoner():
    """Test the reasoner model loading"""
    print("Testing reasoner model loading...")
    
    reasoner = Reasoner()
    
    try:
        # This should trigger model loading
        result = await reasoner.analyze("Test query")
        print("Model loaded successfully!")
        print("Result:", result)
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_reasoner())
    if success:
        print("\nReasoner test passed!")
    else:
        print("\nReasoner test failed.")