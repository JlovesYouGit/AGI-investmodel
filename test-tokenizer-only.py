#!/usr/bin/env python3
"""
Simple script to test tokenizer loading only
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def test_tokenizer_only():
    """Test tokenizer loading only"""
    print("Testing tokenizer loading...")
    
    # Set the working directory to the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    print(f"Working directory: {project_root}")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Set environment variables for local cache
    os.environ['HF_HOME'] = str(project_root / 'huggingface')
    os.environ['HF_HUB_ENABLE_HF_XET'] = '1'
    print(f"HF_HOME: {os.environ['HF_HOME']}")
    print(f"HF_TOKEN set: {'HF_TOKEN' in os.environ}")
    
    try:
        print("Loading tokenizer...")
        from transformers import AutoTokenizer
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME'],
            force_download=False,  # Don't force download, use cache if available
            local_files_only=False  # Allow downloading if needed
        )
        print("✓ Tokenizer loaded successfully")
        
        # Test tokenization
        test_input = "Hello, world!"
        tokens = tokenizer(test_input)
        print(f"✓ Tokenization successful: {tokens}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tokenizer_only()
    if success:
        print("\n🎉 Tokenizer test passed!")
    else:
        print("\n❌ Tokenizer test failed.")