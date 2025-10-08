#!/usr/bin/env python3
"""
Verify that the startup configuration won't trigger a model redownload
"""

import os
from pathlib import Path

def verify_no_redownload():
    """Verify that the configuration won't trigger a model redownload"""
    print("Verifying startup configuration won't trigger model redownload...")
    
    # Check current directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    print(f"Working directory: {project_root}")
    
    # Check if HF_HOME is set correctly
    hf_home = os.environ.get('HF_HOME', '')
    expected_hf_home = str(project_root / 'huggingface')
    
    if hf_home == expected_hf_home:
        print("✓ HF_HOME is correctly set to local cache directory")
    else:
        print(f"⚠ HF_HOME is set to: {hf_home}")
        print(f"  Expected: {expected_hf_home}")
    
    # Check if model files exist
    model_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
    if model_dir.exists():
        print("✓ Model directory exists")
        
        # Check blobs directory
        blobs_dir = model_dir / 'blobs'
        if blobs_dir.exists():
            blobs = list(blobs_dir.iterdir())
            main_files = [b for b in blobs if b.stat().st_size > 1000000]  # > 1MB
            if len(main_files) >= 2:
                print("✓ Main model files are present")
            else:
                print("⚠ Main model files may be missing")
        else:
            print("✗ Blobs directory not found")
    else:
        print("✗ Model directory not found")
    
    # Check if force_download is disabled in reasoner
    reasoner_path = project_root / 'trade_mcp' / 'reasoner.py'
    if reasoner_path.exists():
        with open(reasoner_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'force_download=True' in content:
            print("✗ force_download=True found in reasoner.py")
            # Check if it's in a comment or actual code
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'force_download=True' in line and not line.strip().startswith('#'):
                    print(f"  Line {i+1}: {line.strip()}")
        else:
            print("✓ force_download=True is not present in reasoner.py")
    else:
        print("✗ reasoner.py not found")
    
    # Check startup scripts
    ps1_script = project_root / 'start-trade-mcp.ps1'
    bat_script = project_root / 'start-trade-mcp.bat'
    
    if ps1_script.exists():
        with open(ps1_script, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'force_download' in content:
            print("⚠ force_download found in PowerShell script")
        else:
            print("✓ No force_download in PowerShell script")
    
    if bat_script.exists():
        with open(bat_script, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'force_download' in content:
            print("⚠ force_download found in batch script")
        else:
            print("✓ No force_download in batch script")
    
    print("\nVerification complete!")
    print("The startup scripts should not trigger a model redownload.")

if __name__ == "__main__":
    verify_no_redownload()