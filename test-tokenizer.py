#!/usr/bin/env python3
"""
Script to test tokenizer loading independently
"""

import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_tokenizer_loading():
    """Test loading the Phi-3-mini tokenizer"""
    try:
        # Import required modules
        from transformers import AutoTokenizer
        
        # Get HF token from environment
        HF_TOKEN = os.getenv("HF_TOKEN", "YOUR_HF_TOKEN_HERE")
        
        logger.info("Testing Phi-3-mini tokenizer loading...")
        
        # Load tokenizer
        logger.info("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            token=HF_TOKEN
        )
        logger.info("Tokenizer loaded successfully")
        
        # Test a simple encoding
        logger.info("Testing simple encoding...")
        test_text = "Hello, how are you?"
        encoded = tokenizer(test_text)
        logger.info(f"Encoded tokens: {encoded}")
        
        decoded = tokenizer.decode(encoded['input_ids'])
        logger.info(f"Decoded text: {decoded}")
        
        logger.info("Tokenizer test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load tokenizer: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tokenizer_loading()
    if success:
        print("\nTokenizer loading test passed!")
    else:
        print("\nTokenizer loading test failed.")
