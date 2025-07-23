#!/usr/bin/env python3
"""
Entry point for AI-Powered Screenshot Analysis application.
Run this script to start the application.
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import time to ensure proper loading
time.sleep(0.1)

from src.main_app import main

if __name__ == "__main__":
    main() 