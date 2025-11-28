#!/usr/bin/env python3
"""
Financial Analytics API Startup Script
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def start_api_server():
    """Start the FastAPI server"""
    try:
        print("Starting Financial Analytics API server...")
        print("Server will be available at: http://localhost:8000")
        print("API Documentation: http://localhost:8000/docs")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start the server
        subprocess.call([sys.executable, "financial_analytics_api.py"])
        
    except KeyboardInterrupt:
        print("\n✅ Server stopped gracefully")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main startup function"""
    print("=" * 60)
    print("Financial Analytics API - Startup Script")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("financial_analytics_api.py").exists():
        print("❌ Error: financial_analytics_api.py not found in current directory")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    print()
    
    # Start server
    start_api_server()

if __name__ == "__main__":
    main()