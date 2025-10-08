#!/usr/bin/env python3
"""
Monitor the force redownload progress
"""

import os
import time
from pathlib import Path

def monitor_redownload():
    """Monitor the force redownload progress"""
    print("Monitoring force redownload progress...")
    print("Press Ctrl+C to stop monitoring")
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    model_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
    blobs_dir = model_dir / 'blobs'
    
    try:
        while True:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("Force Redownload Progress Monitor")
            print("=" * 40)
            
            if blobs_dir.exists():
                blobs = list(blobs_dir.iterdir())
                incomplete_files = [b for b in blobs if b.name.endswith('.incomplete')]
                
                if incomplete_files:
                    print("Incomplete downloads:")
                    for blob in incomplete_files:
                        size = blob.stat().st_size
                        # Try to identify which file this is
                        if '3f311787aa136e858556caa8543015161edcad85ba81b6a36072443d7fa73c87' in str(blob):
                            expected_size = 4.97 * 1024 * 1024 * 1024  # 4.97 GB
                            name = "model-00001-of-00002.safetensors"
                        elif 'b7492726c01287bf6e13c3d74c65ade3d436d50da1cf5bb6925bc962419d6610' in str(blob):
                            expected_size = 2.67 * 1024 * 1024 * 1024  # 2.67 GB
                            name = "model-00002-of-00002.safetensors"
                        else:
                            expected_size = None
                            name = blob.name
                        
                        if expected_size:
                            percentage = (size / expected_size) * 100
                            print(f"  {name}: {size / (1024*1024):.2f} MB / {expected_size / (1024*1024*1024):.2f} GB ({percentage:.1f}%)")
                        else:
                            print(f"  {name}: {size / (1024*1024):.2f} MB")
                else:
                    print("✅ All files downloaded successfully!")
                    print("You can now test the model loading.")
                    break
            else:
                print("Blobs directory not found yet")
            
            print(f"\nLast updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("Checking again in 30 seconds...")
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")

if __name__ == "__main__":
    monitor_redownload()