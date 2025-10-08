"""Playwright browser wrapper with auto-respawn functionality."""

import logging
from typing import Optional

from playwright.async_api import async_playwright, Browser, Page

logger = logging.getLogger(__name__)


class BrowserManager:
    """Manages Playwright browser instance with auto-respawn capability."""
    
    def __init__(self):
        """Initialize the browser manager."""
        self.browser: Optional[Browser] = None
        self.playwright = None
        self.failure_count = 0
        self.max_failures = 3
        
    async def start(self):
        """Start the browser instance."""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            logger.info("Browser started successfully")
            self.failure_count = 0
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            self.failure_count += 1
            if self.failure_count >= self.max_failures:
                raise SystemExit(1)
    
    async def get_page(self) -> Page:
        """Get a new browser page, respawning if necessary."""
        if not self.browser or not self.browser.is_connected():
            await self.start()
        return await self.browser.new_page()
    
    async def health_check(self) -> bool:
        """Perform health check of the browser."""
        try:
            if not self.browser or not self.browser.is_connected():
                return False
                
            page = await self.browser.new_page()
            await page.goto("https://finance.yahoo.com", wait_until='domcontentloaded', timeout=5000)
            await page.close()
            return True
        except Exception as e:
            logger.error(f"Browser health check failed: {e}")
            self.failure_count += 1
            if self.failure_count >= self.max_failures:
                raise SystemExit(1)
            return False
    
    async def close(self):
        """Close the browser instance."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


# Global browser manager instance
browser_manager = BrowserManager()