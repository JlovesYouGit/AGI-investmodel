#!/usr/bin/env python3
"""
Test model loading with cache fix
"""

import os
import sys
from pathlib import Path

# Set up environment
os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')

def main():
    print("=== Model Loading Test with Fix ===")
    
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        cache_dir = os.environ.get('HF_HOME')
        model_name = "microsoft/Phi-3-mini-4k-instruct"
        
        print("1. Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            local_files_only=True
        )
        print("✅ Tokenizer loaded successfully")
        
        print("2. Loading model with cache workaround...")
        # Try loading with specific parameters to avoid the cache issue
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            local_files_only=True,
            device_map="cpu",
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True,
            attn_implementation="eager"  # This should help avoid the cache issue
        )
        print("✅ Model loaded successfully")
        
        print("3. Testing simple inference...")
        test_input = "What do you think about NVDA stock?"
        inputs = tokenizer(test_input, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=50, do_sample=False)
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✅ Inference successful")
        print(f"   Result: {result}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())