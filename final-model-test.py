#!/usr/bin/env python3
"""
Final test to verify the model loading works correctly
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()
project_root = Path(__file__).parent
os.chdir(project_root)
os.environ['HF_HOME'] = str(project_root / 'huggingface')

print("Testing model loading...")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    import torch
    
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        cache_dir=os.environ['HF_HOME'],
        local_files_only=True  # Only use local files
    )
    print("✓ Tokenizer loaded successfully")
    
    print("Setting up quantization...")
    # Use 4-bit quantization with nf4 for CPU compatibility
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",  # Use nf4 for CPU compatibility
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16
    )
    print("✓ Quantization config set up")
    
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        quantization_config=quantization_config,
        device_map="auto",
        cache_dir=os.environ['HF_HOME'],
        local_files_only=True  # Only use local files
    )
    print("✓ Model loaded successfully!")
    
    print("\nTesting inference...")
    # Test a simple inference
    test_input = "The future of AI trading is"
    inputs = tokenizer(test_input, return_tensors="pt")
    
    # Generate output
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=20,
            temperature=0.7,
            do_sample=True
        )
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"✓ Inference successful!")
    print(f"Input: {test_input}")
    print(f"Output: {result}")
    
    print("\n🎉 ALL TESTS PASSED! The model is working correctly.")
    print("You can now start the Trade-MCP application without redownloading the model.")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
