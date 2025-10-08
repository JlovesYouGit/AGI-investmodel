#!/usr/bin/env python3
"""
Script to check the status of the model download
"""

import os
from pathlib import Path

def check_download_status():
    """Check the status of the model download"""
    print("Checking model download status...")
    
    # Set the working directory to the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    print(f"Working directory: {project_root}")
    
    # Check if the model directory exists
    model_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
    if not model_dir.exists():
        print("Model directory not found")
        return False
    
    print(f"Model directory: {model_dir}")
    
    # Check the blobs directory
    blobs_dir = model_dir / 'blobs'
    if blobs_dir.exists():
        print("Blobs directory exists")
        blobs = list(blobs_dir.iterdir())
        print(f"Number of blobs: {len(blobs)}")
        for blob in blobs:
            size = blob.stat().st_size
            print(f"  {blob.name}: {size / (1024*1024):.2f} MB")
    else:
        print("Blobs directory not found")
    
    # Check the snapshots directory
    snapshots_dir = model_dir / 'snapshots'
    if snapshots_dir.exists():
        print("Snapshots directory exists")
        snapshots = list(snapshots_dir.iterdir())
        print(f"Number of snapshots: {len(snapshots)}")
        for snapshot in snapshots:
            print(f"  {snapshot.name}")
    else:
        print("Snapshots directory not found")
    
    return True

if __name__ == "__main__":
    check_download_status()