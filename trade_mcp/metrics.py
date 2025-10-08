"""Prometheus metrics for the Trade-MCP application."""

from prometheus_client import Counter, Gauge, Histogram

# Define metrics
insider_rows = Counter('insider_rows', 'Number of insider trading rows processed')
browser_crashes = Counter('browser_crashes', 'Number of browser crashes')
accuracy_retries = Counter('accuracy_retries', 'Number of accuracy gate retries')
orders_total = Counter('orders_total', 'Total number of trading orders', ['action'])
portfolio_value = Gauge('portfolio_value', 'Current portfolio value')
response_time = Histogram('response_time', 'Response time of trading decisions')

# Health metrics
browser_health = Gauge('browser_health', 'Browser health status (1=healthy, 0=unhealthy)')
telegram_health = Gauge('telegram_health', 'Telegram connection health (1=healthy, 0=unhealthy)')
mcp_health = Gauge('mcp_health', 'MCP server health (1=healthy, 0=unhealthy)')