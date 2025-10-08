#!/usr/bin/env python3
"""
Script to clear and redownload the Phi-3-mini model.
This can help resolve issues with corrupted or partially downloaded models.
"""

import os
import shutil
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_hf_cache_dir():
    """Get the Hugging Face cache directory."""
    cache_dir = os.environ.get('HF_HOME')
    if not cache_dir:
        cache_dir = os.path.join(os.getcwd(), 'huggingface')
    return Path(cache_dir)

def clear_model_cache():
    """Clear the Phi-3-mini model from cache."""
    cache_dir = get_hf_cache_dir()
    model_cache_path = cache_dir / "hub" / "models--microsoft--Phi-3-mini-4k-instruct"
    
    if model_cache_path.exists():
        logger.info(f"Removing model cache at {model_cache_path}")
        try:
            shutil.rmtree(model_cache_path)
            logger.info("Model cache cleared successfully")
        except Exception as e:
            logger.error(f"Failed to remove model cache: {e}")
            return False
    else:
        logger.info("Model cache not found, nothing to clear")
    
    # Also clear any offload folder
    offload_path = Path("offload")
    if offload_path.exists():
        logger.info(f"Removing offload folder at {offload_path}")
        try:
            shutil.rmtree(offload_path)
            logger.info("Offload folder cleared successfully")
        except Exception as e:
            logger.error(f"Failed to remove offload folder: {e}")
    
    return True

def redownload_model():
    """Redownload the Phi-3-mini model."""
    logger.info("Redownloading Phi-3-mini model...")
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        # Get cache directory
        cache_dir = get_hf_cache_dir()
        logger.info(f"Using cache directory: {cache_dir}")
        
        # Download tokenizer
        logger.info("Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=str(cache_dir),
            resume_download=False,  # Force fresh download
            local_files_only=False
        )
        logger.info("Tokenizer downloaded successfully")
        
        # Download model
        logger.info("Downloading model...")
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            cache_dir=str(cache_dir),
            resume_download=False,  # Force fresh download
            local_files_only=False,
            device_map={"": "cpu"},  # Force CPU usage for compatibility
            attn_implementation="eager"  # Use eager attention implementation for CPU compatibility
        )
        logger.info("Model downloaded successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to redownload model: {e}")
        return False

def main():
    """Main function to clear and redownload the model."""
    logger.info("Starting model clear and redownload process...")
    
    # Clear existing model cache
    if not clear_model_cache():
        logger.error("Failed to clear model cache, aborting")
        return False
    
    # Redownload model
    if not redownload_model():
        logger.error("Failed to redownload model")
        return False
    
    logger.info("Model clear and redownload process completed successfully!")
    logger.info("You can now restart the Trade-MCP application.")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)