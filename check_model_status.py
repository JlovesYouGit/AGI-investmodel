#!/usr/bin/env python3
"""
Check model status and files
"""

import os
import sys
from pathlib import Path

def main():
    print("=== Model Status Check ===")
    
    # Check model directory
    model_base_dir = Path('huggingface/models--microsoft--Phi-3-mini-4k-instruct')
    print(f"Model base directory exists: {model_base_dir.exists()}")
    
    if model_base_dir.exists():
        # Check blobs
        blobs_dir = model_base_dir / 'blobs'
        print(f"Blobs directory exists: {blobs_dir.exists()}")
        
        if blobs_dir.exists():
            blobs = list(blobs_dir.iterdir())
            print(f"Found {len(blobs)} blob files")
            
            # Check for main model files
            main_files = [b for b in blobs if b.stat().st_size > 1000000]  # > 1MB
            print(f"Found {len(main_files)} main model files:")
            for f in main_files:
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"  - {f.name[:32]}: {size_mb:.2f} MB")
        
        # Check snapshots
        snapshots_dir = model_base_dir / 'snapshots'
        print(f"Snapshots directory exists: {snapshots_dir.exists()}")
        
        if snapshots_dir.exists():
            snapshots = list(snapshots_dir.iterdir())
            print(f"Found {len(snapshots)} snapshot(s)")
            for snapshot in snapshots:
                print(f"  - {snapshot.name}")
                
                # Check snapshot contents
                if snapshot.is_dir():
                    snapshot_files = list(snapshot.iterdir())
                    safetensor_files = [f for f in snapshot_files if f.suffix == '.safetensors']
                    print(f"    Contains {len(snapshot_files)} files ({len(safetensor_files)} safetensor files)")
    
    # Check if there are any incomplete downloads
    if blobs_dir.exists():
        incomplete = list(blobs_dir.glob('*.incomplete'))
        print(f"Incomplete downloads: {len(incomplete)}")
        for f in incomplete:
            print(f"  - {f.name}")
    
    print("\n=== Environment Check ===")
    print(f"HF_HOME: {os.environ.get('HF_HOME', 'Not set')}")
    
    # Try to load config only
    try:
        from transformers import AutoConfig
        config = AutoConfig.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ.get('HF_HOME', 'huggingface'),
            local_files_only=True
        )
        print(f"✅ Model config loaded successfully")
        print(f"   Model type: {config.model_type}")
        print(f"   Hidden size: {getattr(config, 'hidden_size', 'N/A')}")
        print(f"   Num layers: {getattr(config, 'num_hidden_layers', 'N/A')}")
    except Exception as e:
        print(f"❌ Error loading model config: {e}")

if __name__ == "__main__":
    main()