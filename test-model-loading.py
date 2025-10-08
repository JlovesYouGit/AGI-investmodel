#!/usr/bin/env python3
"""
Simple script to test if the Phi-3-mini model can be loaded correctly.
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def test_model_loading():
    """Test if the model can be loaded correctly."""
    print("Testing Phi-3-mini model loading...")
    
    # Set cache directory
    cache_dir = os.environ.get('HF_HOME', os.path.join(os.getcwd(), 'huggingface'))
    print(f"Using cache directory: {cache_dir}")
    
    try:
        print("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=cache_dir,
            local_files_only=False,
            trust_remote_code=True
        )
        print("Tokenizer loaded successfully!")
        
        print("Loading model...")
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            device_map={"": "cpu"},
            cache_dir=cache_dir,
            local_files_only=False,
            trust_remote_code=True,
            attn_implementation="eager",
            torch_dtype=torch.float32
        )
        print("Model loaded successfully!")
        
        # Test a simple inference
        print("Testing simple inference...")
        prompt = "The quick brown fox"
        inputs = tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=10)
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Generated text: {result}")
        
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model_loading()
    if success:
        print("\nModel loading test completed successfully!")
    else:
        print("\nModel loading test failed!")
    exit(0 if success else 1)