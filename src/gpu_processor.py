"""
GPU-accelerated image processing and OCR functionality.
Handles image preprocessing, text extraction, and GPU optimization.
"""

import time
from .imports import *

class GPUProcessor:
    """Handles GPU-accelerated image processing and OCR operations."""
    
    def __init__(self):
        self.easyocr_reader = None
        self.initialize_gpu_components()
    
    def initialize_gpu_components(self):
        """Initialize GPU-optimized components and OCR engines."""
        print("Initializing GPU-optimized components...")
        
        if TORCH_AVAILABLE and torch.cuda.is_available():
            print(f"Using GPU: {torch.cuda.get_device_name(0)}")
            print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            
            # Warm up GPU
            dummy_tensor = torch.randn(100, 100).to(DEVICE)
            _ = torch.matmul(dummy_tensor, dummy_tensor.T)
            print("GPU warmed up")
        
        if EASYOCR_AVAILABLE and TORCH_AVAILABLE:
            try:
                # Initialize EasyOCR with GPU support
                gpu = torch.cuda.is_available()
                self.easyocr_reader = easyocr.Reader(['en'], gpu=gpu)
                print(f"EasyOCR initialized with GPU: {gpu}")
            except Exception as e:
                print(f"Failed to initialize EasyOCR with GPU: {e}")
                self.easyocr_reader = None
        
        # Set Tesseract path
        if OCR_AVAILABLE:
            try:
                pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
                # Test if tesseract is installed
                pytesseract.get_tesseract_version()
                print("Tesseract OCR engine found and working")
            except Exception as e:
                print(f"WARNING: Tesseract not working: {e}")
                print(f"Make sure Tesseract is installed at: {TESSERACT_PATH}")
        
        if CV2_AVAILABLE and CV2_CUDA_AVAILABLE:
            print("OpenCV CUDA support initialized")
        
        print("GPU components initialized successfully!")
    
    def preprocess_image_gpu(self, img):
        """GPU-accelerated image preprocessing for better OCR results."""
        if not CV2_AVAILABLE:
            return img
        
        try:
            # Convert PIL to OpenCV format
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            if CV2_CUDA_AVAILABLE:
                # Upload to GPU
                gpu_img = cv2.cuda_GpuMat()
                gpu_img.upload(img_cv)
                
                # GPU-accelerated preprocessing pipeline
                # Convert to grayscale on GPU
                gpu_gray = cv2.cuda.cvtColor(gpu_img, cv2.COLOR_BGR2GRAY)
                
                # GPU-accelerated Gaussian blur for noise reduction
                gpu_blur = cv2.cuda.GaussianBlur(gpu_gray, (3, 3), 0)
                
                # GPU-accelerated adaptive thresholding
                gpu_thresh = cv2.cuda.adaptiveThreshold(
                    gpu_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                )
                
                # Download from GPU
                processed_img = gpu_thresh.download()
                
                # Convert back to PIL
                return Image.fromarray(processed_img)
            else:
                # CPU fallback with OpenCV
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (3, 3), 0)
                thresh = cv2.adaptiveThreshold(
                    blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                )
                return Image.fromarray(thresh)
                
        except Exception as e:
            print(f"GPU preprocessing failed: {e}")
            return img
    
    def extract_text_gpu(self, img):
        """Extract text from image using GPU-optimized OCR engines."""
        try:
            print("Extracting text with GPU acceleration...")
            
            text = ""
            
            # Try pytesseract first (faster for simple text)
            if OCR_AVAILABLE:
                try:
                    text = pytesseract.image_to_string(img)
                    print("Used pytesseract for OCR")
                except Exception as e:
                    print(f"pytesseract failed: {e}")
                    text = ""
            
            # Fallback to GPU-optimized easyocr
            if not text and EASYOCR_AVAILABLE and self.easyocr_reader:
                try:
                    # Convert PIL Image to numpy array for easyocr
                    img_array = np.array(img)
                    results = self.easyocr_reader.readtext(img_array)
                    text_lines = []
                    for (bbox, detected_text, prob) in results:
                        if prob > 0.5:  # Only include high confidence text
                            text_lines.append(detected_text)
                    text = "\n".join(text_lines)
                    print("Used GPU-optimized EasyOCR for OCR")
                except Exception as e:
                    print(f"GPU EasyOCR failed: {e}")
                    text = ""
            
            # Clean up the text
            lines = text.strip().split('\n')
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            
            # If no OCR worked, show a message
            if not cleaned_lines:
                cleaned_lines = ["No text detected - GPU OCR libraries may need setup"]
                print("[INFO] No text found - consider installing GPU-enabled OCR libraries")
            
            print(f"[TEXT] Found {len(cleaned_lines)} text lines")
            if cleaned_lines:
                print(f"[TEXT] Sample text: {cleaned_lines[0][:50]}{'...' if len(cleaned_lines[0]) > 50 else ''}")
            
            return cleaned_lines
            
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] GPU OCR error: {error_msg}")
            return ["Error extracting text"]
    
    def get_gpu_status(self):
        """Get current GPU status and capabilities."""
        status = {
            'torch_available': TORCH_AVAILABLE,
            'cuda_available': TORCH_AVAILABLE and torch.cuda.is_available(),
            'opencv_cuda': CV2_CUDA_AVAILABLE,
            'easyocr_gpu': EASYOCR_AVAILABLE and self.easyocr_reader is not None,
            'tesseract_available': OCR_AVAILABLE
        }
        
        if status['cuda_available']:
            status['gpu_name'] = torch.cuda.get_device_name(0)
            status['gpu_memory'] = f"{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB"
        
        return status 