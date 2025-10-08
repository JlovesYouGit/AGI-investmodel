#!/usr/bin/env python3
"""
Wait for huggingface-cli download to complete and then test model loading
"""

import os
import time
from pathlib import Path

def wait_for_download():
    """Wait for huggingface-cli download to complete"""
    print("Waiting for huggingface-cli download to complete...")
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    model_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
    blobs_dir = model_dir / 'blobs'
    
    # Expected file sizes (in bytes) and their corresponding blob names
    # Corrected mapping based on actual file sizes
    expected_files = {
        '3f311787aa136e858556caa8543015161edcad85ba81b6a36072443d7fa73c87.incomplete': {
            'name': 'model-00002-of-00002.safetensors',
            'size': 2669692552  # ~2.67 GB
        },
        'b7492726c01287bf6e13c3d74c65ade3d436d50da1cf5bb6925bc962419d6610.incomplete': {
            'name': 'model-00001-of-00002.safetensors',
            'size': 4972489328  # ~4.97 GB
        }
    }
    
    while True:
        if blobs_dir.exists():
            incomplete_files = list(blobs_dir.glob('*.incomplete'))
            if not incomplete_files:
                print("✅ Download completed successfully!")
                break
            else:
                print(f"⏳ Still downloading... {len(incomplete_files)} files incomplete")
                for f in incomplete_files:
                    current_size = f.stat().st_size
                    file_info = expected_files.get(f.name, {})
                    if file_info:
                        expected_size = file_info['size']
                        file_name = file_info['name']
                        percentage = (current_size / expected_size) * 100
                        print(f"  - {file_name}: {current_size / (1024*1024):.2f} MB / {expected_size / (1024*1024):.2f} MB ({percentage:.1f}%)")
                    else:
                        print(f"  - {f.name}: {current_size / (1024*1024):.2f} MB")
        else:
            print("⏳ Waiting for download to start...")
        
        time.sleep(30)  # Check every 30 seconds
    
    # Test model loading
    test_model_loading()

def test_model_loading():
    """Test model loading after download completes"""
    print("\nTesting model loading...")
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        from dotenv import load_dotenv
        
        # Load environment
        load_dotenv()
        project_root = Path(__file__).parent
        os.environ['HF_HOME'] = str(project_root / 'huggingface')
        
        print("1. Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME'],
            local_files_only=True  # Only use local files
        )
        print("✓ Tokenizer loaded successfully")
        
        print("2. Loading model with CPU-friendly configuration...")
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME'],
            local_files_only=True,  # Only use local files
            device_map="cpu",  # Force CPU usage
            torch_dtype=torch.float32,  # Use float32 for CPU
            low_cpu_mem_usage=True,  # Reduce memory usage during loading
        )
        print("✓ Model loaded successfully")
        
        print("3. Testing simple inference...")
        test_input = "The future of AI is"
        inputs = tokenizer(test_input, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=10,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✓ Inference successful: {result}")
        
        print("\n🎉 MODEL LOADING SUCCESSFUL!")
        print("The model is working correctly with CPU-friendly configuration.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    wait_for_download()