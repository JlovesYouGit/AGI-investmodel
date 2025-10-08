#!/usr/bin/env python3
"""
Script to monitor the model download progress
"""

import os
import time
from pathlib import Path

def monitor_download():
    """Monitor the model download progress"""
    print("Monitoring model download progress...")
    print("Press Ctrl+C to stop monitoring")
    
    # Set the working directory to the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    print(f"Working directory: {project_root}")
    
    try:
        while True:
            # Clear the screen (works on Windows)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("Model Download Progress Monitor")
            print("=" * 40)
            
            # Check if the model directory exists
            model_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
            if not model_dir.exists():
                print("Model directory not found")
                time.sleep(10)
                continue
            
            # Check the blobs directory
            blobs_dir = model_dir / 'blobs'
            if blobs_dir.exists():
                blobs = list(blobs_dir.iterdir())
                incomplete_files = [blob for blob in blobs if blob.name.endswith('.incomplete')]
                
                if incomplete_files:
                    print("Incomplete downloads:")
                    for blob in incomplete_files:
                        size = blob.stat().st_size
                        # Try to get the expected size from the filename
                        expected_size = None
                        if '3f311787aa136e858556caa8543015161edcad85ba81b6a36072443d7fa73c87' in blob.name:
                            expected_size = 2.67 * 1024 * 1024 * 1024  # 2.67 GB
                        elif 'b7492726c01287bf6e13c3d74c65ade3d436d50da1cf5bb6925bc962419d6610' in blob.name:
                            expected_size = 4.97 * 1024 * 1024 * 1024  # 4.97 GB
                        
                        if expected_size:
                            percentage = (size / expected_size) * 100
                            print(f"  {blob.name}: {size / (1024*1024):.2f} MB / {expected_size / (1024*1024*1024):.2f} GB ({percentage:.1f}%)")
                        else:
                            print(f"  {blob.name}: {size / (1024*1024):.2f} MB")
                else:
                    print("All files downloaded successfully!")
                    break
            else:
                print("Blobs directory not found")
            
            # Wait before next check
            print(f"\nLast updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("Checking again in 30 seconds...")
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")

if __name__ == "__main__":
    monitor_download()