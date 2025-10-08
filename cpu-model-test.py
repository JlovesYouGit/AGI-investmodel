#!/usr/bin/env python3
"""
Test model loading with CPU-specific configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()
project_root = Path(__file__).parent
os.chdir(project_root)
os.environ['HF_HOME'] = str(project_root / 'huggingface')

print("Testing model loading with CPU-specific configuration...")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    import torch
    
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=os.environ['HF_HOME'],
        local_files_only=True  # Only use local files
    )
    print("✓ Tokenizer loaded successfully")
    
    print("Setting up CPU-compatible quantization...")
    # Use 4-bit quantization with nf4 for CPU compatibility
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",  # Use nf4 for CPU compatibility
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
        llm_int8_enable_fp32_cpu_offload=True  # Enable CPU offloading
    )
    print("✓ Quantization config set up")
    
    print("Loading model with CPU device map...")
    # Use a simple CPU device map
    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        quantization_config=quantization_config,
        device_map={"": "cpu"},  # Force CPU usage
        cache_dir=os.environ['HF_HOME'],
        local_files_only=True,  # Only use local files
        torch_dtype=torch.float32  # Use float32 for CPU
    )
    print("✓ Model loaded successfully!")
    
    print("\n🎉 MODEL LOADING TEST PASSED!")
    print("The model can be loaded correctly with CPU configuration.")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()