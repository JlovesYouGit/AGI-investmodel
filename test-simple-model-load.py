#!/usr/bin/env python3
"""
Simple test to load the model with minimal configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()
project_root = Path(__file__).parent
os.chdir(project_root)
os.environ['HF_HOME'] = str(project_root / 'huggingface')

print("Testing simple model loading...")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=os.environ['HF_HOME'],
        local_files_only=True  # Only use local files
    )
    print("✓ Tokenizer loaded successfully")
    
    print("Loading model with minimal configuration...")
    # Try loading with minimal configuration first
    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=os.environ['HF_HOME'],
        local_files_only=True,  # Only use local files
        device_map="cpu",  # Force CPU usage
        torch_dtype=torch.float32  # Use float32 for CPU
    )
    print("✓ Model loaded successfully!")
    
    print("\nTesting simple inference...")
    # Test a very simple inference
    test_input = "Hello"
    inputs = tokenizer(test_input, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=5,
            do_sample=False
        )
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"✓ Simple inference successful: {result}")
    
    print("\n🎉 SIMPLE MODEL LOADING TEST PASSED!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()