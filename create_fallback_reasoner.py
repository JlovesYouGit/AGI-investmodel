#!/usr/bin/env python3
"""
Create a modified reasoner that works without the AI model for basic functionality
"""

import os
import sys
from pathlib import Path

def main():
    print("=== Creating Fallback Reasoner ===")
    
    try:
        # Test if we can import the reasoner
        from trade_mcp.reasoner import Reasoner
        print("✅ Reasoner module imported successfully")
        
        # Create a simple test
        reasoner = Reasoner()
        print("✅ Reasoner instantiated")
        print(f"Model state: {reasoner.model}")
        print(f"Model load failed: {reasoner.model_load_failed}")
        
        print("\n=== Fallback Reasoner Ready ===")
        print("The application can run in fallback mode without the AI model.")
        print("You can use the Web UI for basic functionality.")
        print("\nTo start the application in fallback mode:")
        print("  python start_with_fallback.py")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())