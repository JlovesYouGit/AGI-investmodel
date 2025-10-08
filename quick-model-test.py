#!/usr/bin/env python3
"""
Quick test to verify the model is working
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()
project_root = Path(__file__).parent
os.chdir(project_root)
os.environ['HF_HOME'] = str(project_root / 'huggingface')

print("Testing if model files exist...")
model_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
if model_dir.exists():
    print("✓ Model directory exists")
    
    # Check blobs
    blobs_dir = model_dir / 'blobs'
    if blobs_dir.exists():
        blobs = list(blobs_dir.iterdir())
        print(f"✓ Found {len(blobs)} blobs")
        
        # Check for the main model files
        main_files = [b for b in blobs if b.stat().st_size > 1000000]  # > 1MB
        print(f"✓ Found {len(main_files)} main model files")
        for f in main_files:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  - {f.name}: {size_mb:.2f} MB")
    else:
        print("✗ Blobs directory not found")
else:
    print("✗ Model directory not found")

print("\nTesting tokenizer loading...")
try:
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=os.environ['HF_HOME'],
        local_files_only=True  # Only use local files, don't download
    )
    print("✓ Tokenizer loaded successfully from local cache")
    
    # Test tokenization
    test_text = "Hello, world!"
    tokens = tokenizer(test_text)
    print(f"✓ Tokenization works: {len(tokens['input_ids'])} tokens")
    
except Exception as e:
    print(f"✗ Error loading tokenizer: {e}")

print("\nModel setup verification complete!")