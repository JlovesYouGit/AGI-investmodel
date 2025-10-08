#!/usr/bin/env python3
"""
Test script to verify that the model can be loaded from the local cache
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def test_local_model_loading():
    """Test that the model can be loaded from the local cache"""
    print("Testing local model loading...")
    
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
        
        # Try to load the tokenizer from local cache
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME'],
            local_files_only=True  # Force loading from local cache only
        )
        print("✓ Tokenizer loaded successfully from local cache")
        
        print("Loading model...")
        from transformers import AutoModelForCausalLM, BitsAndBytesConfig
        import torch
        
        # Use 4-bit quantization with nf4 for CPU compatibility
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",  # Use nf4 for CPU compatibility
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16
        )
        
        # Try to load the model (allow downloading if needed)
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            quantization_config=quantization_config,
            device_map="auto",
            cache_dir=os.environ['HF_HOME'],
            local_files_only=False  # Allow downloading if needed
        )
        print("✓ Model loaded successfully from local cache")
        
        # Test a simple inference
        print("Testing inference...")
        test_input = "Hello, world!"
        inputs = tokenizer(test_input, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=10)
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✓ Inference successful: {result[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_local_model_loading()
    if success:
        print("\n🎉 All tests passed! The model is properly configured in the local cache.")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
        sys.exit(1)