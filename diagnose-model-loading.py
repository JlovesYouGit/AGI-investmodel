#!/usr/bin/env python3
"""
Diagnose model loading issues
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()
project_root = Path(__file__).parent
os.chdir(project_root)
os.environ['HF_HOME'] = str(project_root / 'huggingface')

print("Diagnosing model loading issues...")
print("=" * 50)

# Check if we're in the correct virtual environment
venv = os.environ.get('VIRTUAL_ENV', '')
if 'venv311' not in venv:
    print("⚠️  Warning: Not in venv311 virtual environment")
    print(f"   Current environment: {venv}")
else:
    print("✓ Using correct virtual environment")

# Check Python version
python_version = sys.version
print(f"Python version: {python_version}")

# Check model files
model_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
if not model_dir.exists():
    print("❌ Model directory not found!")
    sys.exit(1)

print(f"Model directory: {model_dir}")

blobs_dir = model_dir / 'blobs'
if blobs_dir.exists():
    blobs = list(blobs_dir.iterdir())
    main_files = [b for b in blobs if b.stat().st_size > 1000000]  # > 1MB
    print(f"Found {len(main_files)} main model files:")
    for f in main_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"  - {f.name[:16]}...: {size_mb:.2f} MB")
else:
    print("❌ Blobs directory not found!")
    sys.exit(1)

# Test loading with different approaches
print("\nTesting different model loading approaches...")
print("=" * 50)

# Approach 1: Simple loading
print("1. Testing simple loading (no quantization)...")
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    
    start_time = time.time()
    print("   Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=os.environ['HF_HOME'],
        local_files_only=True
    )
    print(f"   ✓ Tokenizer loaded in {time.time() - start_time:.2f} seconds")
    
    print("   Loading model with CPU device map...")
    start_time = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=os.environ['HF_HOME'],
        local_files_only=True,
        device_map={"": "cpu"},
        torch_dtype=torch.float32
    )
    print(f"   ✓ Model loaded in {time.time() - start_time:.2f} seconds")
    
    print("   Testing simple inference...")
    start_time = time.time()
    test_input = "Hello"
    inputs = tokenizer(test_input, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=5, do_sample=False)
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"   ✓ Inference completed in {time.time() - start_time:.2f} seconds")
    print(f"   Result: {result}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Diagnosis complete!")