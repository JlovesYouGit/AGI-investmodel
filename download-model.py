#!/usr/bin/env python3
"""
Script to download the Phi-3-mini model using Hugging Face CLI for faster downloads
"""

import os
import subprocess
import sys
from pathlib import Path

def download_model():
    """Download the Phi-3-mini model using Hugging Face CLI"""
    print("Downloading Phi-3-mini model using Hugging Face CLI...")
    
    # Set environment variables
    os.environ['HF_HUB_ENABLE_HF_XET'] = '1'
    os.environ['HF_HOME'] = os.path.join(os.getcwd(), 'huggingface')
    
    # Ensure the cache directory exists
    cache_dir = Path(os.environ['HF_HOME'])
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Use huggingface-cli to download the model
        cmd = [
            'huggingface-cli', 'download',
            'microsoft/Phi-3-mini-4k-instruct',
            '--cache-dir', str(cache_dir),
            '--token', os.environ.get('HF_TOKEN', 'YOUR_HF_TOKEN_HERE')
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)  # 2 hour timeout
        
        if result.returncode == 0:
            print("Model downloaded successfully!")
            print(result.stdout)
            return True
        else:
            print("Error downloading model:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("Download timed out after 1 hour")
        return False
    except Exception as e:
        print(f"Error during download: {e}")
        return False

if __name__ == "__main__":
    success = download_model()
    if success:
        print("\nModel download completed successfully!")
        print("You can now start the Trade-MCP application.")
    else:
        print("\nModel download failed.")
        print("Please check your internet connection and try again.")
