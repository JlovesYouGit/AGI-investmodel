"""Configuration module for Trade-MCP."""

import os
from pathlib import Path

# API Keys
HF_TOKEN = os.getenv("HF_TOKEN", "YOUR_HF_TOKEN_HERE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_TOKEN_HERE")
CAPITAL = os.getenv("CAPITAL", "5000")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")

# Model Configuration
PHI3_MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
LLAMA3_MODEL_NAME = "llama3:8b-instruct-q4_K_M"

# Paths
DATA_DIR = Path(os.getenv("DATA_DIR", ".data"))
LOGS_DIR = DATA_DIR / "logs"
LORA_DIR = DATA_DIR / "lora"
CHATLOG_FILE = DATA_DIR / "chatlog.jsonl"
AUDIO_EMOTION_FILE = DATA_DIR / "audio_emotion.jsonl"
CAPITAL_FILE = DATA_DIR / "portfolio.json"

# Fine-tuning
FINETUNE_INTERVAL_HOURS = 6
FINETUNE_MIN_ROWS = 100

# Insider Trading
INSIDER_REFRESH_INTERVAL_MINUTES = 30

# Web UI
WEBUI_HOST = os.getenv("WEBUI_HOST", "127.0.0.1")  # Changed from hardcoded "0.0.0.0" to use environment variable
WEBUI_PORT = 7863  # Default port (will be overridden by dynamic port finder)

# Prometheus
PROMETHEUS_HOST = os.getenv("PROMETHEUS_HOST", "127.0.0.1")  # Changed from hardcoded "0.0.0.0" to use environment variable
PROMETHEUS_PORT = 9090

# Browser
BROWSER_HOST = "localhost"
BROWSER_PORT = 9222
