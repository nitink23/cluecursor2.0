#!/usr/bin/env python3
"""
Test setup script for AI-Powered Screenshot Analyzer.
Run this to verify your installation and OpenAI API setup.
"""

import os
import sys
import time
import dotenv

dotenv.load_dotenv()

def test_imports():
    """Test that all required imports are available."""
    print("🔍 Testing imports...")
    
    try:
        import tkinter as tk
        print("✓ tkinter available")
    except ImportError:
        print("✗ tkinter not available")
        return False
    
    try:
        import openai
        print("✓ openai library available")
    except ImportError:
        print("✗ openai library not available - run: pip install openai")
        return False
    
    try:
        import PIL
        print("✓ PIL/Pillow available")
    except ImportError:
        print("✗ PIL/Pillow not available - run: pip install Pillow")
        return False
    
    try:
        import pyautogui
        print("✓ pyautogui available")
    except ImportError:
        print("✗ pyautogui not available - run: pip install pyautogui")
        return False
    
    return True

def test_api_key():
    """Test OpenAI API key setup."""
    print("\n🔑 Testing OpenAI API key...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("✗ OPENAI_API_KEY environment variable not set")
        print("  Set it with: set OPENAI_API_KEY=your-api-key-here (Windows)")
        print("  Or: export OPENAI_API_KEY=your-api-key-here (Linux/Mac)")
        return False
    
    if len(api_key) < 20:
        print("✗ OPENAI_API_KEY seems too short")
        return False
    
    print("✓ OPENAI_API_KEY found and looks valid")
    return True

def test_openai_connection():
    """Test OpenAI API connection."""
    print("\n🌐 Testing OpenAI API connection...")
    
    try:
        import openai
        client = openai.OpenAI()
        
        # Test with a simple models list call
        models = client.models.list()
        model_names = [model.id for model in models]
        
        if 'gpt-4o' in model_names:
            print("✓ OpenAI API connection successful")
            print("✓ GPT-4o model accessible")
            return True
        elif 'gpt-4-vision-preview' in model_names:
            print("✓ OpenAI API connection successful")
            print("⚠ GPT-4o not found, but GPT-4 Vision available")
            return True
        else:
            print("⚠ OpenAI API connected but vision models not found")
            print("  Available models:", len(model_names))
            print("  First few models:", model_names[:3])
            return False
            
    except Exception as e:
        print(f"✗ OpenAI API connection failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🤖 AI Screenshot Analyzer - Setup Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please install missing dependencies.")
        return False
    
    # Test API key
    if not test_api_key():
        print("\n❌ API key test failed. Please set your OpenAI API key.")
        return False
    
    # Test API connection
    if not test_openai_connection():
        print("\n❌ API connection test failed. Please check your API key and internet connection.")
        return False
    
    print("\n✅ All tests passed! Your setup is ready.")
    print("\nTo run the application:")
    print("  python run.py")
    print("\nControls:")
    print("  - ESC: Close")
    print("  - Ctrl+A: Manual analysis")
    print("  - Ctrl+M: Change mode")
    print("  - Ctrl+P: Custom prompt")
    
    return True

if __name__ == "__main__":
    main() 