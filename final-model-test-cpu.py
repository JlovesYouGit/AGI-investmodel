#!/usr/bin/env python3
"""
Final test to load the model with CPU-specific optimizations
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def final_model_test():
    """Final test to load the model with CPU-specific optimizations"""
    print("Final model loading test with CPU-specific optimizations...")
    
    # Load environment
    load_dotenv()
    project_root = Path(__file__).parent
    os.chdir(project_root)
    os.environ['HF_HOME'] = str(project_root / 'huggingface')
    
    try:
        print("1. Loading tokenizer...")
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME'],
            local_files_only=True  # Only use local files
        )
        print("✓ Tokenizer loaded successfully")
        
        print("2. Loading model with maximum CPU optimizations...")
        from transformers import AutoModelForCausalLM
        import torch
        
        # Use maximum CPU-friendly settings
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=os.environ['HF_HOME'],
            local_files_only=True,  # Only use local files
            device_map="cpu",  # Force CPU usage
            torch_dtype=torch.float32,  # Use float32 for CPU
            low_cpu_mem_usage=True,  # Reduce memory usage during loading
        )
        print("✓ Model loaded successfully")
        
        print("3. Testing simple inference...")
        test_input = "The future of AI is"
        inputs = tokenizer(test_input, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=10,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✓ Inference successful: {result}")
        
        print("\n🎉 FINAL MODEL TEST PASSED!")
        print("The model is working correctly with maximum CPU optimizations.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = final_model_test()
    if success:
        print("\n🎉 SUCCESS: Model loading issue has been resolved!")
        print("\nYou can now start the Trade-MCP application:")
        print("  .\\start-trade-mcp.ps1")
        print("\nOr test the full application with:")
        print("  python -m trade_mcp")
    else:
        print("\n❌ The model loading issue persists.")
        print("Please check the errors above for more information.")