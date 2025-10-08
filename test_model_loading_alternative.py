#!/usr/bin/env python3
"""
Alternative approach to test model loading with more specific parameters
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up environment
os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')
os.environ['HF_HUB_ENABLE_HF_XET'] = '1'
os.environ['TRANSFORMERS_OFFLOAD_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'offload')

print("=== Alternative Model Loading Test ===")

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    cache_dir = os.environ.get('HF_HOME')
    
    print("1. Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=cache_dir,
        local_files_only=True,
        trust_remote_code=True
    )
    print("✅ Tokenizer loaded successfully")
    
    print("2. Loading model with alternative configuration...")
    # Try loading with specific parameters for CPU-only systems
    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=cache_dir,
        local_files_only=True,
        device_map="cpu",
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        attn_implementation="eager",
        use_safetensors=True
    )
    print("✅ Model loaded successfully")
    
    print("3. Testing simple inference...")
    test_input = "The future of AI is"
    inputs = tokenizer(test_input, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=20, do_sample=False)
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"✅ Inference successful: {result}")
    
    print("\n🎉 Alternative model loading test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()