"""Health check endpoint for the Trade-MCP application."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .browser import browser_manager
from .bot import telegram_alive
from .mcp_server import mcp_server_alive

app = FastAPI()


@app.get("/healthz")
async def health_check() -> JSONResponse:
    """Health check endpoint that verifies all components are alive."""
    try:
        # Check browser health
        browser_healthy = await browser_manager.health_check()
        
        # Check if all components are alive
        telegram_status = telegram_alive()
        mcp_status = mcp_server_alive()
        
        # Log the status of each component for debugging
        print(f"Browser healthy: {browser_healthy}")
        print(f"Telegram alive: {telegram_status}")
        print(f"MCP server alive: {mcp_status}")
        
        if browser_healthy and telegram_status and mcp_status:
            return JSONResponse(
                status_code=200,
                content={"status": "healthy", "components": {
                    "browser": browser_healthy,
                    "telegram": telegram_status,
                    "mcp_server": mcp_status
                }}
            )
        else:
            raise HTTPException(status_code=503, detail=f"Service unhealthy - Browser: {browser_healthy}, Telegram: {telegram_status}, MCP: {mcp_status}")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")