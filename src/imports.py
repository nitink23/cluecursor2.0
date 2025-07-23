"""
Import management and library detection for AI-powered screenshot analysis.
Handles conditional imports and provides fallbacks for missing libraries.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time
import mss
import base64
from PIL import Image, ImageGrab
import io
import os
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
    print("✓ Environment variables loaded from .env file")
except ImportError:
    DOTENV_AVAILABLE = False
    print("⚠ python-dotenv not available - using system environment variables only")

# Try to import OpenAI
try:
    import openai
    OPENAI_AVAILABLE = True
    print("✓ OpenAI library available")
except ImportError:
    OPENAI_AVAILABLE = False
    print("✗ OpenAI library not available - please install: pip install openai")

# Try to import requests for HTTP calls
try:
    import requests
    REQUESTS_AVAILABLE = True
    print("✓ requests library available")
except ImportError:
    REQUESTS_AVAILABLE = False
    print("✗ requests library not available")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
    print("✓ numpy available")
except ImportError:
    NUMPY_AVAILABLE = False
    print("✗ numpy not available")

# Basic image processing with OpenCV (for optional preprocessing)
try:
    import cv2
    CV2_AVAILABLE = True
    print("✓ OpenCV available for image preprocessing")
except ImportError:
    CV2_AVAILABLE = False
    print("✗ OpenCV not available")

# Check for OpenAI API key
API_KEY_AVAILABLE = bool(os.getenv('OPENAI_API_KEY'))
if API_KEY_AVAILABLE:
    print("✓ OpenAI API key found in environment")
else:
    print("⚠ OpenAI API key not found - set OPENAI_API_KEY in .env file or environment variable")

# Configuration constants
DEFAULT_WINDOW_SIZE = (450, 600)
MIN_WINDOW_SIZE = (350, 300)
MAX_WINDOW_SIZE = (800, 1200)

# OpenAI Configuration (can be overridden by .env file)
DEFAULT_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '500'))
TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7')) 