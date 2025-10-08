# Use NVIDIA CUDA base image
FROM nvidia/cuda:12.1-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-pip \
    python3.11-venv \
    git \
    curl \
    wget \
    build-essential \
    cmake \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libx11-xcb1 \
    libxss1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Conda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Set PATH
ENV PATH="/opt/conda/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy environment file
COPY environment.yml .

# Create conda environment
RUN conda env create -f environment.yml

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install whisper.cpp
RUN git clone https://github.com/ggerganov/whisper.cpp.git && \
    cd whisper.cpp && \
    make

# Install Playwright browsers
RUN npm install -g playwright
RUN playwright install chromium

# Make port 8080 available
EXPOSE 8080

# Make port 9090 available for Prometheus
EXPOSE 9090

# Make port 9222 available for Playwright
EXPOSE 9222

# Copy application code
COPY . .

# Activate conda environment and run the application
CMD ["conda", "run", "--no-capture-output", "-n", "trade-mcp", "python", "-m", "trade_mcp"]