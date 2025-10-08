#!/usr/bin/env python3
"""
Script to check the health of Trade-MCP components
"""

import requests
import time
import subprocess
import sys
from pathlib import Path

def check_health_endpoint():
    """Check the health endpoint"""
    try:
        response = requests.get("http://localhost:8081/healthz", timeout=5)
        print(f"Health endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Health endpoint is responding")
            health_data = response.json()
            print(f"  Browser alive: {health_data.get('browser_alive', 'Unknown')}")
            print(f"  Telegram alive: {health_data.get('telegram_alive', 'Unknown')}")
            print(f"  MCP server alive: {health_data.get('mcp_alive', 'Unknown')}")
            return True
        else:
            print("✗ Health endpoint returned error")
            print(f"  Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Health endpoint is not accessible (connection refused)")
        return False
    except Exception as e:
        print(f"✗ Health endpoint check failed: {e}")
        return False

def check_webui():
    """Check if Web UI is accessible"""
    try:
        response = requests.get("http://localhost:7861", timeout=5)
        print(f"Web UI status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Web UI is accessible")
            return True
        else:
            print("✗ Web UI returned error")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Web UI is not accessible (connection refused)")
        return False
    except Exception as e:
        print(f"✗ Web UI check failed: {e}")
        return False

def check_process():
    """Check if the main process is running"""
    try:
        # This is a simple check - in a real scenario, you might want to check for specific process names
        result = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=10)
        if "python" in result.stdout.lower():
            print("✓ Python processes are running")
            return True
        else:
            print("✗ No Python processes found")
            return False
    except Exception as e:
        print(f"✗ Process check failed: {e}")
        return False

def main():
    """Main health check function"""
    print("Trade-MCP Health Check")
    print("=" * 30)
    
    checks = [
        ("Process Check", check_process),
        ("Health Endpoint", check_health_endpoint),
        ("Web UI", check_webui),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"✗ {name} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 30)
    print("Summary:")
    if all(results):
        print("✓ All checks passed - Trade-MCP is healthy")
        return 0
    else:
        failed_checks = [checks[i][0] for i, result in enumerate(results) if not result]
        print(f"✗ Some checks failed: {', '.join(failed_checks)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Trade-MCP is running (use start-app.bat or start-app.ps1)")
        print("2. Check the logs for any error messages")
        print("3. Verify all required environment variables are set")
        print("4. Ensure no port conflicts exist")
        return 1

if __name__ == "__main__":
    sys.exit(main())