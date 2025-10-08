#!/usr/bin/env python3
"""
Script to verify that the Hugging Face cache is properly configured in the current directory
"""

import os
from pathlib import Path

def verify_hf_cache():
    """Verify that the Hugging Face cache is properly configured"""
    print("Verifying Hugging Face cache configuration...")
    
    # Get current working directory
    cwd = Path.cwd()
    print(f"Current working directory: {cwd}")
    
    # Check if HF_HOME is set
    hf_home = os.environ.get('HF_HOME')
    if hf_home:
        print(f"HF_HOME environment variable: {hf_home}")
        hf_home_path = Path(hf_home)
        if hf_home_path.exists():
            print("✓ HF_HOME directory exists")
        else:
            print("✗ HF_HOME directory does not exist")
    else:
        print("HF_HOME environment variable is not set")
        # Default to current directory + huggingface
        hf_home_path = cwd / "huggingface"
        print(f"Defaulting to: {hf_home_path}")
    
    # Check if huggingface directory exists in current directory
    local_hf_dir = cwd / "huggingface"
    if local_hf_dir.exists():
        print("✓ Local huggingface directory exists")
        # List contents
        try:
            contents = list(local_hf_dir.iterdir())
            print(f"  Contents: {[item.name for item in contents]}")
        except Exception as e:
            print(f"  Error listing contents: {e}")
    else:
        print("✗ Local huggingface directory does not exist")
    
    # Check if we're in the correct virtual environment
    venv = os.environ.get('VIRTUAL_ENV')
    if venv:
        print(f"Virtual environment: {venv}")
        expected_venv = str(cwd / "venv311")
        if venv == expected_venv:
            print("✓ Correct virtual environment is active")
        else:
            print(f"✗ Unexpected virtual environment. Expected: {expected_venv}")
    else:
        print("No virtual environment is active")

if __name__ == "__main__":
    verify_hf_cache()