#!/usr/bin/env python3
"""
Test loading model using load_checkpoint_and_dispatch for better memory management
"""

import os
import sys
from pathlib import Path

# Set up environment
os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')
os.environ['TRANSFORMERS_OFFLOAD_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'offload')

print("=== Checkpoint Loading Test ===")

try:
    import torch
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
    from accelerate import init_empty_weights, load_checkpoint_and_dispatch
    
    cache_dir = os.environ.get('HF_HOME')
    
    print("1. Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=cache_dir,
        local_files_only=True,
        trust_remote_code=True
    )
    print("✅ Tokenizer loaded successfully")
    
    print("2. Creating empty model...")
    config = AutoConfig.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=cache_dir,
        local_files_only=True,
        trust_remote_code=True
    )
    
    with init_empty_weights():
        model = AutoModelForCausalLM.from_config(config, trust_remote_code=True)
    print("✅ Empty model created successfully")
    
    print("3. Loading checkpoint with dispatch...")
    model_path = os.path.join(cache_dir, "models--microsoft--Phi-3-mini-4k-instruct", "snapshots", "0a67737cc96d2554230f90338b163bc6380a2a85")
    
    model = load_checkpoint_and_dispatch(
        model,
        model_path,
        device_map="cpu",
        dtype=torch.float32,
        offload_folder="offload",
        offload_state_dict=True
    )
    print("✅ Model checkpoint loaded successfully")
    
    print("4. Testing simple inference...")
    test_input = "The future of AI is"
    inputs = tokenizer(test_input, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=20, do_sample=False)
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"✅ Inference successful: {result}")
    
    print("\n🎉 Checkpoint loading test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()