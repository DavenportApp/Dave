#!/usr/bin/env python3
"""
CAM Assistant Launcher Script

This script launches the CAM Assistant Streamlit application.
Run this file to start the application in your web browser.
"""

import subprocess
import sys
import os


def main():
    """Launch the CAM Assistant application."""
    print("🚀 Starting CAM Assistant REV8...")
    print("📍 Opening in web browser at http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Run the Streamlit application
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "cam_assistant_REV8.py",
            "--server.port=8501",
            "--server.headless=false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 CAM Assistant stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running CAM Assistant: {e}")
        print("💡 Make sure you have installed the requirements:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
