#!/usr/bin/env python3
"""
Completely clear cache and redownload model with huggingface-cli
"""

import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def complete_redownload():
    """Completely clear cache and redownload model with huggingface-cli"""
    print("Completely clearing cache and redownloading model...")
    
    # Load environment
    load_dotenv()
    project_root = Path(__file__).parent
    os.chdir(project_root)
    os.environ['HF_HOME'] = str(project_root / 'huggingface')
    
    # Clear the entire cache
    cache_dir = project_root / 'huggingface'
    if cache_dir.exists():
        print(f"Clearing entire cache directory: {cache_dir}")
        try:
            shutil.rmtree(cache_dir)
            print("✓ Cache cleared successfully")
        except Exception as e:
            print(f"❌ Error clearing cache: {e}")
            return False
    else:
        print("Cache directory not found, proceeding with download")
    
    # Create cache directory
    cache_dir.mkdir(exist_ok=True)
    os.environ['HF_HOME'] = str(cache_dir)
    
    # Try to download with huggingface-cli
    try:
        print("Downloading model with huggingface-cli...")
        cmd = [
            'huggingface-cli', 'download',
            'microsoft/Phi-3-mini-4k-instruct',
            '--cache-dir', str(cache_dir),
            '--token', os.environ.get('HF_TOKEN', 'YOUR_HF_TOKEN_HERE')
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)  # 2 hour timeout
        
        if result.returncode == 0:
            print("✓ Model downloaded successfully with huggingface-cli!")
            print(result.stdout)
            return True
        else:
            print("❌ Error downloading model with huggingface-cli:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Download timed out after 2 hours")
        return False
    except Exception as e:
        print(f"❌ Error during download: {e}")
        return False

if __name__ == "__main__":
    success = complete_redownload()
    if success:
        print("\n🎉 Complete redownload successful!")
        print("You can now test the model loading.")
    else:
        print("\n❌ Complete redownload failed.")
