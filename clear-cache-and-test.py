#!/usr/bin/env python3
"""
Script to clear the model cache and test model loading with correct quantization
"""

import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

def clear_cache_and_test():
    """Clear the model cache and test model loading"""
    print("Clearing model cache and testing model loading...")
    
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
    
    # Clear the model cache
    model_cache_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
    if model_cache_dir.exists():
        print(f"Clearing model cache directory: {model_cache_dir}")
        try:
            shutil.rmtree(model_cache_dir)
            print("✓ Model cache cleared successfully")
        except Exception as e:
            print(f"✗ Error clearing model cache: {e}")
            return False
    else:
        print("Model cache directory not found")
    
    # Now try to load the model
    try:
        print("Loading tokenizer...")
        from transformers import AutoTokenizer
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME']
        )
        print("✓ Tokenizer loaded successfully")
        
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
        
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            quantization_config=quantization_config,
            device_map="auto",
            cache_dir=os.environ['HF_HOME']
        )
        print("✓ Model loaded successfully")
        
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
    success = clear_cache_and_test()
    if success:
        print("\n🎉 Model loaded successfully!")
    else:
        print("\n❌ Model loading failed.")