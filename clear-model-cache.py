#!/usr/bin/env python3
"""
Script to clear Hugging Face model cache, particularly for Phi-3-mini model
"""

import os
import shutil
from pathlib import Path

def clear_phi3_cache():
    """Clear the Phi-3-mini model cache"""
    # Get HF cache directory
    hf_home = os.environ.get('HF_HOME', os.path.expanduser('~/.cache/huggingface'))
    hub_cache = Path(hf_home) / 'hub'
    
    print(f"HF cache location: {hf_home}")
    print(f"Hub cache exists: {hub_cache.exists()}")
    
    if not hub_cache.exists():
        print("Hub cache directory does not exist")
        return
    
    # Look for Phi-3-mini model cache
    phi3_cache = hub_cache / 'models--microsoft--Phi-3-mini-4k-instruct'
    
    if phi3_cache.exists():
        print(f"Found Phi-3-mini cache: {phi3_cache}")
        response = input("Do you want to delete this cache? (y/N): ")
        if response.lower() == 'y':
            try:
                shutil.rmtree(phi3_cache)
                print("Phi-3-mini cache cleared successfully")
            except Exception as e:
                print(f"Error clearing cache: {e}")
        else:
            print("Cache clearing cancelled")
    else:
        print("Phi-3-mini cache not found")
    
    # Also check for any other potentially problematic cache
    print("\nOther model caches found:")
    for item in hub_cache.iterdir():
        if item.is_dir() and item.name.startswith('models--'):
            print(f"  - {item.name}")

if __name__ == "__main__":
    clear_phi3_cache()