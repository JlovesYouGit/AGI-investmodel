#!/bin/bash

# Trade-MCP Installation Script for Linux
# This script installs all dependencies and starts the application

set -e

echo "Installing Trade-MCP..."

# Install system dependencies
if command -v apt-get &> /dev/null; then
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv git curl wget build-essential cmake
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    sudo yum install -y python3 python3-pip git curl wget gcc gcc-c++ make cmake
elif command -v pacman &> /dev/null; then
    # Arch Linux
    sudo pacman -Syu python python-pip git curl wget base-devel cmake
else
    echo "Unsupported package manager. Please install dependencies manually."
    exit 1
fi

# Install Miniconda
echo "Installing Miniconda..."
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda3
export PATH="$HOME/miniconda3/bin:$PATH"

# Install Ollama
echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Clone whisper.cpp
echo "Installing whisper.cpp..."
if [ ! -d "whisper.cpp" ]; then
    git clone https://github.com/ggerganov/whisper.cpp.git
fi
cd whisper.cpp
make
cd ..

# Install Playwright browsers
echo "Installing Playwright browsers..."
npm install -g playwright
playwright install chromium

# Create conda environment
echo "Creating conda environment..."
conda env create -f environment.yml

# Activate environment and install package
echo "Installing Trade-MCP..."
conda activate trade-mcp
pip install -e .

# Pull required models
echo "Pulling required models..."
ollama pull llama3:8b-instruct-q4_K_M

echo "Installation complete!"
echo "To start the service, run: docker compose up -d"