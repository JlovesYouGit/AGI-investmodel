#!/usr/bin/env python3
"""
Comprehensive diagnostic for model loading issues
"""

import os
import sys
import time
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up environment
os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')
os.environ['HF_HUB_ENABLE_HF_XET'] = '1'
os.environ['TRANSFORMERS_OFFLOAD_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'offload')

print("=== Model Loading Diagnostic ===")
print(f"Working directory: {os.getcwd()}")
print(f"HF_HOME: {os.environ.get('HF_HOME', 'Not set')}")
print(f"Python version: {sys.version}")

# Check model files
model_dir = Path('huggingface/models--microsoft--Phi-3-mini-4k-instruct')
print(f"\nModel directory exists: {model_dir.exists()}")

if model_dir.exists():
    blobs_dir = model_dir / 'blobs'
    print(f"Blobs directory exists: {blobs_dir.exists()}")
    
    if blobs_dir.exists():
        blobs = list(blobs_dir.iterdir())
        print(f"Found {len(blobs)} blob files")
        
        # Check for main model files
        main_files = [b for b in blobs if b.stat().st_size > 1000000]  # > 1MB
        print(f"Found {len(main_files)} main model files (>1MB):")
        for f in main_files:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  - {f.name[:32]}: {size_mb:.2f} MB")

print("\n=== Testing Model Loading ===")

try:
    import torch
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import asyncio
    
    async def test_model_loading():
        cache_dir = os.environ.get('HF_HOME')
        
        print("\n1. Loading tokenizer...")
        start_time = time.time()
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                "microsoft/Phi-3-mini-4k-instruct",
                cache_dir=cache_dir,
                local_files_only=True,  # Only use local files to verify download
                trust_remote_code=True
            )
            elapsed = time.time() - start_time
            print(f"✅ Tokenizer loaded successfully in {elapsed:.2f} seconds")
        except Exception as e:
            print(f"❌ Error loading tokenizer: {e}")
            return False
        
        print("\n2. Loading model with CPU-optimized configuration...")
        start_time = time.time()
        try:
            model = AutoModelForCausalLM.from_pretrained(
                "microsoft/Phi-3-mini-4k-instruct",
                cache_dir=cache_dir,
                local_files_only=True,  # Only use local files
                device_map={"": "cpu"},  # Force CPU usage
                torch_dtype=torch.float32,  # Use float32 for CPU
                low_cpu_mem_usage=True,  # Reduce memory usage during loading
                trust_remote_code=True,
                attn_implementation="eager"
            )
            elapsed = time.time() - start_time
            print(f"✅ Model loaded successfully in {elapsed:.2f} seconds")
            
            print("\n3. Testing simple inference...")
            test_input = "Hello, world!"
            inputs = tokenizer(test_input, return_tensors="pt")
            
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=10, do_sample=False)
            
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f"✅ Inference successful: {result}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # Run with timeout
    try:
        result = asyncio.run(asyncio.wait_for(test_model_loading(), timeout=120.0))
        if result:
            print("\n🎉 Model loading diagnostic completed successfully!")
        else:
            print("\n💥 Model loading diagnostic failed!")
    except asyncio.TimeoutError:
        print("\n⏰ Model loading timed out after 120 seconds!")
    except Exception as e:
        print(f"\n💥 Model loading failed with error: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"Error during setup: {e}")
    import traceback
    traceback.print_exc()