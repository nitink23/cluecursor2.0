"""
Main application class for GPU-optimized screen capture OCR.
Orchestrates all components and manages the application lifecycle.
"""

import tkinter as tk
from .imports import *
from .gpu_processor import GPUProcessor
from .ui_components import UIComponents
from .screen_capture import ScreenCapture
from .cursor_tracker import CursorTracker

class GPUScreenCaptureApp:
    """Main application class for GPU-optimized screen capture OCR."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Initialize components
        self.gpu_processor = GPUProcessor()
        self.ui = UIComponents(self.root, *DEFAULT_WINDOW_SIZE)
        self.cursor_tracker = CursorTracker(self.root, self.ui)
        self.screen_capture = ScreenCapture(self.gpu_processor, self.ui)
        
        # Setup callbacks and bindings
        self.setup_callbacks()
        self.setup_bindings()
        
        # Update UI with GPU status
        self.update_gpu_status()
        
        # Start components
        self.cursor_tracker.start_tracking()
        
        # Auto-start capture after 2 seconds
        self.root.after(2000, self.screen_capture.start_capture_loop)
    
    def setup_window(self):
        """Setup the main window properties."""
        self.root.title("GPU-Optimized Screen Capture Overlay")
        
        # Make the window transparent and always on top
        self.root.attributes('-alpha', 0.85)
        self.root.attributes('-topmost', True)
        
        # Remove window decorations
        self.root.overrideredirect(True)
    
    def setup_callbacks(self):
        """Setup UI callbacks."""
        self.ui.set_capture_callback(self.screen_capture.toggle_capture)
        self.ui.set_close_callback(self.root.destroy)
    
    def setup_bindings(self):
        """Setup keyboard bindings."""
        # Bind escape key to close
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # Bind Ctrl+C to toggle capture
        self.root.bind('<Control-c>', lambda e: self.screen_capture.toggle_capture())
    
    def update_gpu_status(self):
        """Update UI with current GPU and OCR status."""
        gpu_status = self.gpu_processor.get_gpu_status()
        
        # Determine GPU status text
        if gpu_status['cuda_available']:
            gpu_text = "GPU"
            ocr_method = "easyocr" if gpu_status['easyocr_gpu'] else "pytesseract" if gpu_status['tesseract_available'] else "None"
        else:
            gpu_text = "CPU"
            ocr_method = "easyocr" if EASYOCR_AVAILABLE else "pytesseract" if OCR_AVAILABLE else "None"
        
        self.ui.update_ocr_label(gpu_text, ocr_method)
        
        # Print status summary
        print("\n=== GPU Status Summary ===")
        print(f"PyTorch: {'✓' if gpu_status['torch_available'] else '✗'}")
        print(f"CUDA: {'✓' if gpu_status['cuda_available'] else '✗'}")
        if gpu_status['cuda_available']:
            print(f"GPU: {gpu_status['gpu_name']}")
            print(f"Memory: {gpu_status['gpu_memory']}")
        print(f"OpenCV CUDA: {'✓' if gpu_status['opencv_cuda'] else '✗'}")
        print(f"EasyOCR GPU: {'✓' if gpu_status['easyocr_gpu'] else '✗'}")
        print(f"Tesseract: {'✓' if gpu_status['tesseract_available'] else '✗'}")
        print("========================\n")
    
    def run(self):
        """Start the application main loop."""
        print("🚀 GPU-Optimized Screen Capture OCR Started!")
        print("Controls:")
        print("  - ESC: Close application")
        print("  - Ctrl+C: Manual capture")
        print("  - Click 'Manual Capture' button")
        print("  - Automatic capture every 2 seconds")
        print()
        
        self.root.mainloop()
    
    def cleanup(self):
        """Cleanup resources before exit."""
        self.screen_capture.stop_capture()
        self.cursor_tracker.stop_tracking()
        print("Application cleanup completed.")

def main():
    """Main entry point for the application."""
    # Disable pyautogui failsafe
    pyautogui.FAILSAFE = False
    
    try:
        app = GPUScreenCaptureApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print(f"Application error: {e}")
    finally:
        if 'app' in locals():
            app.cleanup()

if __name__ == "__main__":
    main() 