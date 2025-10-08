#!/usr/bin/env python3
"""
Minimal test for model loading with absolute minimal configuration
"""

import os
import sys
from pathlib import Path

# Set up environment
os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')

print("=== Minimal Model Loading Test ===")

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    cache_dir = os.environ.get('HF_HOME')
    
    print("1. Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=cache_dir,
        local_files_only=True
    )
    print("✅ Tokenizer loaded successfully")
    
    print("2. Loading model with minimal configuration...")
    # Try the most minimal configuration possible
    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=cache_dir,
        local_files_only=True,
        device_map="cpu",
        torch_dtype=torch.float32
    )
    print("✅ Model loaded successfully")
    
    print("\n🎉 Minimal model loading test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()