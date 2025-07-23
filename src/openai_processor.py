"""
OpenAI processor for analyzing screenshots using GPT-4o Vision API.
Handles image processing and AI-powered analysis.
"""

import base64
import io
from PIL import Image
import openai
from .imports import *
import dotenv

dotenv.load_dotenv()

class OpenAIProcessor:
    """Handles OpenAI API calls for screenshot analysis."""
    
    def __init__(self, api_key=None):
        """Initialize OpenAI processor with API key."""
        self.client = openai.OpenAI(api_key=api_key) if api_key else openai.OpenAI()
        self.model = DEFAULT_MODEL  # Uses GPT-4o by default
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        
    def encode_image(self, image, max_size=1024, quality=85):
        """Convert PIL Image to base64 string for OpenAI API with optimization."""
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Optimize image size for API (reduces token usage)
            width, height = image.size
            if width > max_size or height > max_size:
                # Calculate new dimensions while maintaining aspect ratio
                if width > height:
                    new_width = max_size
                    new_height = int(height * (max_size / width))
                else:
                    new_height = max_size
                    new_width = int(width * (max_size / height))
                
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"[INFO] Image resized from {width}x{height} to {new_width}x{new_height}")
            
            # Save to bytes buffer with optimization
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=quality, optimize=True)
            buffer.seek(0)
            
            # Encode to base64
            image_bytes = buffer.getvalue()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            print(f"[INFO] Image encoded: {len(image_base64)} characters, ~{len(image_bytes)} bytes")
            return image_base64
        except Exception as e:
            print(f"[ERROR] Failed to encode image: {e}")
            return None
    
    def analyze_screenshot(self, image, prompt=None, detail="auto"):
        """Analyze screenshot using GPT-4o Vision API with configurable detail level."""
        if prompt is None:
            prompt = """Analyze this screenshot and provide insights about what you see. 
            Focus on:
            - Main content and purpose
            - Important text or information
            - UI elements or interface details
            - Any notable patterns or data
            Keep the response concise but informative."""
        
        try:
            # Encode image with optimization
            image_base64 = self.encode_image(image)
            if not image_base64:
                return "Failed to process image"
            
            # Make API call using chat completions
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}",
                                    "detail": detail  # "auto", "low", or "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = f"OpenAI API error: {str(e)}"
            print(f"[ERROR] {error_msg}")
            return error_msg
    
    def extract_text(self, image):
        """Extract and organize text from screenshot."""
        prompt = """Extract all visible text from this screenshot. 
        Organize it in a clear, readable format. 
        Preserve the structure and hierarchy of the content.
        If there are multiple sections, separate them clearly."""
        
        return self.analyze_screenshot(image, prompt)
    
    def describe_ui(self, image):
        """Describe the user interface elements in the screenshot."""
        prompt = """Describe the user interface elements in this screenshot.
        Focus on:
        - Buttons, menus, and interactive elements
        - Layout and design patterns
        - Navigation structure
        - Key functionality visible
        - Color scheme and visual hierarchy
        Be specific about locations and element types."""
        
        return self.analyze_screenshot(image, prompt)
    
    def summarize_content(self, image):
        """Summarize the main content of the screenshot."""
        prompt = """Provide a concise summary of the main content in this screenshot.
        Focus on:
        - Primary purpose or function
        - Key information displayed
        - Main topics or themes
        - Important data or metrics
        - Overall context and significance
        Keep it brief but comprehensive."""
        
        return self.analyze_screenshot(image, prompt)
    
    def custom_analysis(self, image, custom_prompt):
        """Perform custom analysis with user-provided prompt."""
        return self.analyze_screenshot(image, custom_prompt)
    
    def get_status(self):
        """Get OpenAI processor status."""
        try:
            # Test API connection with a simple call
            response = self.client.models.list()
            available_models = [model.id for model in response]
            
            return {
                'api_available': True,
                'model': self.model,
                'models_accessible': len(available_models) > 0,
                'gpt4o_available': 'gpt-4o' in available_models,
                'available_models': available_models[:5]  # Show first 5 models
            }
        except Exception as e:
            return {
                'api_available': False,
                'model': self.model,
                'error': str(e)
            } 