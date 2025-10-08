#!/usr/bin/env python3
"""
Test loading a single model shard to diagnose issues
"""

import os
import sys
from pathlib import Path

# Set up environment
os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'huggingface')

print("=== Single Shard Loading Test ===")

try:
    import torch
    import safetensors
    
    # Find the model directory
    model_base_dir = Path('huggingface/models--microsoft--Phi-3-mini-4k-instruct')
    
    # Find the snapshot directory
    snapshots_dir = model_base_dir / 'snapshots'
    if snapshots_dir.exists():
        snapshot_dirs = list(snapshots_dir.iterdir())
        if snapshot_dirs:
            snapshot_dir = snapshot_dirs[0]
            print(f"Using snapshot: {snapshot_dir.name}")
            
            # Look for safetensor files
            safetensor_files = list(snapshot_dir.glob("*.safetensors"))
            print(f"Found {len(safetensor_files)} safetensor files")
            
            if safetensor_files:
                # Try to load the first shard
                shard_file = safetensor_files[0]
                print(f"Attempting to load shard: {shard_file.name}")
                
                # Try to open the safetensor file
                with safetensors.safe_open(str(shard_file), framework="pt", device="cpu") as f:
                    print(f"✅ Safetensor file opened successfully")
                    print(f"Keys in shard: {list(f.keys())[:10]}...")  # Show first 10 keys
                    print(f"Total keys: {len(list(f.keys()))}")
                    
                    # Try to load a few tensors
                    keys = list(f.keys())[:3]  # Load first 3 tensors
                    for key in keys:
                        tensor = f.get_tensor(key)
                        print(f"  - {key}: {tensor.shape}")
                        
                print("✅ Single shard loading test completed successfully!")
            else:
                print("❌ No safetensor files found")
        else:
            print("❌ No snapshots found")
    else:
        print("❌ Snapshots directory not found")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()