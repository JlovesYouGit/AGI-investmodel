#!/usr/bin/env python3
"""
Test model loading after download completes
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def test_model_loading():
    """Test model loading after download completes"""
    print("Testing model loading after download...")
    
    # Load environment
    load_dotenv()
    project_root = Path(__file__).parent
    os.chdir(project_root)
    os.environ['HF_HOME'] = str(project_root / 'huggingface')
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        print("1. Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME'],
            local_files_only=True  # Only use local files to verify download
        )
        print("✓ Tokenizer loaded successfully")
        
        print("2. Loading model with CPU-friendly configuration...")
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME'],
            local_files_only=True,  # Only use local files
            device_map={"": "cpu"},  # Force CPU usage
            torch_dtype=torch.float32  # Use float32 for CPU
        )
        print("✓ Model loaded successfully")
        
        print("3. Testing simple inference...")
        test_input = "The future of AI trading is"
        inputs = tokenizer(test_input, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=20, do_sample=False)
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✓ Inference successful: {result}")
        
        print("\n🎉 MODEL LOADING TEST PASSED!")
        print("The model is working correctly with CPU-friendly configuration.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model_loading()
    if success:
        print("\nYou can now start the Trade-MCP application:")
        print("  .\\start-trade-mcp.ps1")
    else:
        print("\nModel loading failed. Check the errors above.")