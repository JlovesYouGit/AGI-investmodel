#!/usr/bin/env python3
"""
Check the integrity of the downloaded model files
"""

import os
from pathlib import Path

def check_model_integrity():
    """Check the integrity of the downloaded model files"""
    print("Checking model file integrity...")
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    model_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
    if not model_dir.exists():
        print("❌ Model directory not found")
        return False
    
    print(f"Model directory: {model_dir}")
    
    # Check blobs directory
    blobs_dir = model_dir / 'blobs'
    if not blobs_dir.exists():
        print("❌ Blobs directory not found")
        return False
    
    blobs = list(blobs_dir.iterdir())
    print(f"Found {len(blobs)} blob files")
    
    # Check for the main model files
    main_files = []
    for blob in blobs:
        if blob.stat().st_size > 1000000:  # > 1MB
            main_files.append(blob)
    
    print(f"Found {len(main_files)} main model files:")
    for f in main_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"  - {f.name}: {size_mb:.2f} MB")
    
    # Check if the main files are the expected checkpoint shards
    expected_shards = [
        '3f311787aa136e858556caa8543015161edcad85ba81b6a36072443d7fa73c87',
        'b7492726c01287bf6e13c3d74c65ade3d436d50da1cf5bb6925bc962419d6610'
    ]
    
    found_shards = []
    for shard in expected_shards:
        shard_path = blobs_dir / shard
        if shard_path.exists():
            found_shards.append(shard)
            print(f"✓ Found expected shard: {shard[:16]}...")
        else:
            print(f"❌ Missing expected shard: {shard[:16]}...")
    
    # Check snapshots directory
    snapshots_dir = model_dir / 'snapshots'
    if snapshots_dir.exists():
        snapshots = list(snapshots_dir.iterdir())
        print(f"Found {len(snapshots)} snapshot(s)")
        for snapshot in snapshots:
            print(f"  - {snapshot.name}")
            
            # Check if snapshot points to valid files
            if snapshot.is_dir():
                snapshot_files = list(snapshot.iterdir())
                print(f"    Contains {len(snapshot_files)} files")
    else:
        print("❌ Snapshots directory not found")
    
    # Try to load the model config to check integrity
    print("\nTesting model config loading...")
    try:
        from transformers import AutoConfig
        config = AutoConfig.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=str(project_root / 'huggingface'),
            local_files_only=True  # Only use local files
        )
        print("✓ Model config loaded successfully")
        print(f"  Model type: {config.model_type}")
        print(f"  Hidden size: {getattr(config, 'hidden_size', 'N/A')}")
        print(f"  Number of layers: {getattr(config, 'num_hidden_layers', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Error loading model config: {e}")
        return False

if __name__ == "__main__":
    success = check_model_integrity()
    if success:
        print("\n🎉 Model integrity check passed!")
    else:
        print("\n❌ Model integrity check failed!")
        print("You may need to clear the cache and redownload the model.")