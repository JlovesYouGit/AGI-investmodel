"""Generate architecture diagram for Trade-MCP."""

from diagrams import Diagram, Cluster
from diagrams.generic.os import Windows, Linux
from diagrams.programming.framework import FastAPI
from diagrams.generic.device import Mobile
from diagrams.generic.storage import Storage
from diagrams.generic.compute import Edge
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.ai import Nginx
from diagrams.onprem.client import Client
from diagrams.onprem.container import Docker


with Diagram("Trade-MCP Architecture", show=False, filename="docs/architecture", outformat="png"):
    with Cluster("User Interface"):
        telegram = Mobile("Telegram Bot")
        webui = Client("Web UI")
    
    with Cluster("Core Services"):
        mcp_server = FastAPI("MCP Server")
        reasoner = Nginx("Reasoning Engine")
        finetune = Edge("Fine-tune Worker")
        browser = Edge("Browser Manager")
        audio = Edge("Audio Processor")
        health = FastAPI("Health Check")
    
    with Cluster("AI Models"):
        phi3 = Nginx("Phi-3 Mini (4-bit)")
        llama3 = Nginx("Llama3 (Ollama)")
    
    with Cluster("Storage"):
        chatlog = Storage("Chat Logs")
        lora = Storage("LoRA Adapters")
        audio_data = Storage("Audio Data")
        portfolio = Storage("Portfolio Data")
    
    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
    
    with Cluster("Containerization"):
        docker = Docker("Docker")
        windows = Windows("Windows 11")
        linux = Linux("Linux")
    
    with Cluster("External Services"):
        openinsider = Edge("openinsider.com")
        yahoo = Edge("finance.yahoo.com")
        ddg = Edge("DuckDuckGo")
    
    # Connections
    telegram >> mcp_server
    webui >> mcp_server
    
    mcp_server >> reasoner
    reasoner >> phi3
    reasoner >> llama3
    
    mcp_server >> browser
    browser >> openinsider
    browser >> yahoo
    
    mcp_server >> finetune
    finetune >> chatlog
    finetune >> lora
    
    mcp_server >> audio
    audio >> audio_data
    
    mcp_server >> health
    
    phi3 >> chatlog
    llama3 >> chatlog
    
    prometheus >> reasoner
    grafana >> prometheus
    
    docker >> mcp_server
    windows >> docker
    linux >> docker
    
    mcp_server >> ddg