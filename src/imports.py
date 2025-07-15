"""
Import management and library detection for GPU-optimized OCR.
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

# Try to import OCR libraries with fallbacks
try:
    import pytesseract
    OCR_AVAILABLE = True
    print("✓ pytesseract available")
except ImportError:
    OCR_AVAILABLE = False
    print("✗ pytesseract not available")

try:
    import easyocr
    EASYOCR_AVAILABLE = True
    print("✓ easyocr available")
except ImportError:
    EASYOCR_AVAILABLE = False
    print("✗ easyocr not available")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
    print("✓ numpy available")
except ImportError:
    NUMPY_AVAILABLE = False
    print("✗ numpy not available")

# GPU-optimized imports
try:
    import torch
    TORCH_AVAILABLE = True
    print("✓ PyTorch available")
    if torch.cuda.is_available():
        print(f"✓ CUDA available - GPU: {torch.cuda.get_device_name(0)}")
        DEVICE = torch.device('cuda')
    else:
        print("⚠ CUDA not available, using CPU")
        DEVICE = torch.device('cpu')
except ImportError:
    TORCH_AVAILABLE = False
    print("✗ PyTorch not available")
    DEVICE = None

try:
    import cv2
    CV2_AVAILABLE = True
    print("✓ OpenCV available")
    # Check if OpenCV was compiled with CUDA support
    if hasattr(cv2, 'cuda') and cv2.cuda.getCudaEnabledDeviceCount() > 0:
        print("✓ OpenCV CUDA support available")
        CV2_CUDA_AVAILABLE = True
    else:
        print("⚠ OpenCV CUDA support not available")
        CV2_CUDA_AVAILABLE = False
except ImportError:
    CV2_AVAILABLE = False
    CV2_CUDA_AVAILABLE = False
    print("✗ OpenCV not available")

# Configuration constants
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
DEFAULT_WINDOW_SIZE = (400, 500)
MIN_WINDOW_SIZE = (300, 200)
MAX_WINDOW_SIZE = (800, 1000) 