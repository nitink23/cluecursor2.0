#!/usr/bin/env python3
"""
Quick test script for OpenAI GPT-4o Vision API
Tests both image analysis and basic functionality
"""

import os
import sys
import base64
import time
from PIL import Image, ImageDraw
import io

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.openai_processor import OpenAIProcessor
    from src.imports import *
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

def create_test_image():
    """Create a simple test image with text"""
    # Create a simple image with text
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    draw.text((20, 50), "TEST IMAGE", fill='black')
    draw.text((20, 80), "This is a test for GPT-4o vision", fill='blue')
    draw.text((20, 110), "Can you read this text?", fill='red')
    
    # Add some shapes
    draw.rectangle([300, 20, 380, 60], outline='green', width=2)
    draw.ellipse([300, 80, 380, 140], outline='purple', width=2)
    
    # Save to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return img_byte_arr.getvalue()

def test_openai_connection():
    """Test basic OpenAI connection"""
    print("🔍 Testing OpenAI Connection...")
    
    try:
        processor = OpenAIProcessor()
        status = processor.get_status()
        
        if status['api_available']:
            print("✅ OpenAI API connection successful!")
            print(f"   Model: {status['model']}")
            if 'gpt4o_available' in status:
                print(f"   GPT-4o available: {'✅' if status['gpt4o_available'] else '❌'}")
            return True
        else:
            print("❌ OpenAI API connection failed!")
            print(f"   Error: {status.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_vision_analysis():
    """Test image analysis with a simple test image"""
    print("\n📸 Testing Vision Analysis...")
    
    try:
        # Create test image
        test_image_data = create_test_image()
        test_image = Image.open(io.BytesIO(test_image_data))
        
        print("   Created test image with text and shapes")
        
        # Initialize processor
        processor = OpenAIProcessor()
        
        # Test basic analysis
        print("   Sending image to GPT-4o...")
        result = processor.analyze_screenshot(test_image, 
            "What text can you read in this image? Also describe any shapes you see.")
        
        print("✅ Vision analysis successful!")
        print(f"   Response: {result[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Vision analysis failed: {e}")
        return False

def test_different_analysis_modes():
    """Test different analysis modes"""
    print("\n🎯 Testing Different Analysis Modes...")
    
    try:
        test_image_data = create_test_image()
        test_image = Image.open(io.BytesIO(test_image_data))
        processor = OpenAIProcessor()
        
        modes = {
            "Text Extraction": "Extract all text from this image",
            "General Analysis": "Describe everything you see in this image",
            "UI Description": "Describe the layout and visual elements"
        }
        
        for mode, prompt in modes.items():
            print(f"   Testing {mode}...")
            result = processor.analyze_screenshot(test_image, prompt)
            print(f"   ✅ {mode}: {result[:100]}...")
            time.sleep(1)  # Rate limiting
            
        return True
        
    except Exception as e:
        print(f"❌ Mode testing failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 OpenAI GPT-4o Vision API Test Suite")
    print("=" * 50)
    
    # Check environment setup
    print("🔑 Checking Environment Setup...")
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("   Make sure your .env file contains: OPENAI_API_KEY=your-key-here")
        return False
    else:
        print(f"✅ OPENAI_API_KEY found (length: {len(api_key)})")
    
    # Run tests
    tests = [
        ("OpenAI Connection", test_openai_connection),
        ("Vision Analysis", test_vision_analysis),
        ("Analysis Modes", test_different_analysis_modes)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print(f"\n🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your OpenAI GPT-4o setup is working perfectly!")
        print("\nYou can now run the main application:")
        print("   python run.py")
    else:
        print("⚠️  Some tests failed. Please check your API key and internet connection.")
        print("   Common issues:")
        print("   - Invalid API key")
        print("   - Insufficient API credits")
        print("   - Network connectivity issues")

if __name__ == "__main__":
    main() 