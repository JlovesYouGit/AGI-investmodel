#!/usr/bin/env python3
"""
Force redownload the model with proper configuration
"""

import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

def force_redownload_model():
    """Force redownload the model with proper configuration"""
    print("Force redownloading model with proper configuration...")
    
    # Load environment
    load_dotenv()
    project_root = Path(__file__).parent
    os.chdir(project_root)
    os.environ['HF_HOME'] = str(project_root / 'huggingface')
    
    # Clear the model cache
    model_cache_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
    if model_cache_dir.exists():
        print(f"Clearing model cache directory: {model_cache_dir}")
        try:
            shutil.rmtree(model_cache_dir)
            print("✓ Model cache cleared successfully")
        except Exception as e:
            print(f"❌ Error clearing model cache: {e}")
            return False
    else:
        print("Model cache directory not found, proceeding with download")
    
    # Now try to download the model with proper configuration
    try:
        print("Downloading model with proper configuration...")
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        # Download tokenizer
        print("Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME']
        )
        print("✓ Tokenizer downloaded successfully")
        
        # Download model with CPU-friendly configuration
        print("Downloading model...")
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME'],
            device_map={"": "cpu"},
            torch_dtype="auto"  # Let transformers choose the best dtype
        )
        print("✓ Model downloaded successfully")
        
        # Test a simple inference
        print("Testing inference...")
        test_input = "Hello, world!"
        inputs = tokenizer(test_input, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=10, do_sample=False)
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✓ Inference successful: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during download: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = force_redownload_model()
    if success:
        print("\n🎉 Model redownloaded successfully!")
        print("You can now start the Trade-MCP application.")
    else:
        print("\n❌ Model redownload failed.")