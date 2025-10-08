#!/usr/bin/env python3
"""
Check if model files can be loaded directly
"""

import os
import torch
from pathlib import Path

def check_model_files():
    """Check if model files can be loaded directly"""
    print("Checking model files directly...")
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    model_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
    blobs_dir = model_dir / 'blobs'
    
    if not blobs_dir.exists():
        print("❌ Blobs directory not found!")
        return False
    
    # Find the main shard files
    main_shards = []
    for blob in blobs_dir.iterdir():
        if blob.name.startswith('3f311787') or blob.name.startswith('b7492726'):
            main_shards.append(blob)
    
    print(f"Found {len(main_shards)} main shard files:")
    for shard in main_shards:
        size_mb = shard.stat().st_size / (1024 * 1024)
        print(f"  - {shard.name[:16]}...: {size_mb:.2f} MB")
    
    # Try to load one shard directly
    if main_shards:
        shard_file = main_shards[0]
        print(f"\nTrying to load shard: {shard_file.name[:16]}...")
        try:
            # Try to load as a safetensor file
            import safetensors
            with safetensors.safe_open(str(shard_file), framework="pt", device="cpu") as f:
                print("✓ Safetensor file can be opened")
                keys = list(f.keys())
                print(f"  Contains {len(keys)} tensors")
                if keys:
                    print(f"  First few keys: {keys[:3]}")
        except ImportError:
            print("⚠️  Safetensors library not available")
        except Exception as e:
            print(f"❌ Error loading safetensor: {e}")
        
        # Try to load as a PyTorch file
        print(f"\nTrying to load as PyTorch file...")
        try:
            data = torch.load(str(shard_file), map_location="cpu")
            print("✓ PyTorch file can be loaded")
            if isinstance(data, dict):
                print(f"  Contains {len(data)} items")
                keys = list(data.keys())
                if keys:
                    print(f"  First few keys: {keys[:3]}")
            else:
                print(f"  Data type: {type(data)}")
        except Exception as e:
            print(f"❌ Error loading PyTorch file: {e}")
            import traceback
            traceback.print_exc()
    
    return True

if __name__ == "__main__":
    check_model_files()