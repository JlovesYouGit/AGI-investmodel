#!/usr/bin/env python3
"""
Script to test if the model download is complete and test model loading
"""

import os
from pathlib import Path

def test_model_completion():
    """Test if the model download is complete and test model loading"""
    print("Testing model download completion and loading...")
    
    # Set the working directory to the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    print(f"Working directory: {project_root}")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Set environment variables for local cache
    os.environ['HF_HOME'] = str(project_root / 'huggingface')
    os.environ['HF_HUB_ENABLE_HF_XET'] = '1'
    print(f"HF_HOME: {os.environ['HF_HOME']}")
    print(f"HF_TOKEN set: {'HF_TOKEN' in os.environ}")
    
    # Check if the model directory exists
    model_dir = project_root / 'huggingface' / 'models--microsoft--Phi-3-mini-4k-instruct'
    if not model_dir.exists():
        print("Model directory not found")
        return False
    
    print(f"Model directory: {model_dir}")
    
    # Check for incomplete downloads
    blobs_dir = model_dir / 'blobs'
    if blobs_dir.exists():
        incomplete_files = list(blobs_dir.glob('*.incomplete'))
        if incomplete_files:
            print("Incomplete downloads found:")
            for f in incomplete_files:
                print(f"  {f.name}")
            print("Download not complete yet.")
            return False
        else:
            print("All files downloaded successfully!")
    
    # Try to load the model
    try:
        print("Loading tokenizer...")
        from transformers import AutoTokenizer
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME']
        )
        print("✓ Tokenizer loaded successfully")
        
        print("Loading model...")
        from transformers import AutoModelForCausalLM, BitsAndBytesConfig
        import torch
        
        # Use 4-bit quantization with nf4 for CPU compatibility
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",  # Use nf4 for CPU compatibility
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16
        )
        
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            quantization_config=quantization_config,
            device_map="auto",
            cache_dir=os.environ['HF_HOME']
        )
        print("✓ Model loaded successfully")
        
        # Test a simple inference
        print("Testing inference...")
        test_input = "The future of AI in trading is"
        inputs = tokenizer(test_input, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=20, temperature=0.7)
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✓ Inference successful: {result}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model_completion()
    if success:
        print("\n🎉 Model download and loading test passed!")
        print("The Trade-MCP application should now work correctly.")
    else:
        print("\n❌ Model download and loading test failed.")
        print("Please wait for the download to complete and try again.")