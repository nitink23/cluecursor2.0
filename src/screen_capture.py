"""
Screen capture functionality for real-time text extraction.
Handles screen grabbing, cursor tracking, and capture scheduling.
"""

import threading
import time
from .imports import *

class ScreenCapture:
    """Handles screen capture and cursor tracking operations."""
    
    def __init__(self, gpu_processor, ui_components):
        self.gpu_processor = gpu_processor
        self.ui = ui_components
        self.last_capture = None
        self.processing = False
        self.capturing = False
        
    def start_capture_loop(self):
        """Start the automatic capture loop."""
        self.capturing = True
        self.ui.update_status("Starting GPU-optimized capture...")
        print("Started GPU-optimized automatic capture mode")
        # Start the first capture after 2 seconds
        self.ui.root.after(2000, self.start_next_capture)
    
    def toggle_capture(self):
        """Manual trigger for screen capture."""
        if not self.processing:
            # Get current cursor position
            x, y = pyautogui.position()
            print(f"\n[MANUAL] Manual GPU capture triggered at cursor position ({x}, {y}) - {time.strftime('%H:%M:%S')}")
            self.capture_around_cursor(x, y)
        else:
            print(f"[BUSY] Still processing previous capture - {time.strftime('%H:%M:%S')}")
    
    def start_next_capture(self):
        """Start the next automatic capture."""
        if self.capturing and not self.processing:
            # Get current cursor position
            x, y = pyautogui.position()
            print(f"\n[AUTO] Starting GPU-optimized capture at cursor position ({x}, {y}) - {time.strftime('%H:%M:%S')}")
            self.capture_around_cursor(x, y)
        elif self.processing:
            print(f"[WAIT] Still processing - will retry in 2 seconds - {time.strftime('%H:%M:%S')}")
            # Retry in 2 seconds if still processing
            self.ui.root.after(2000, self.start_next_capture)
    
    def capture_around_cursor(self, cursor_x, cursor_y):
        """Capture area around cursor and extract text."""
        if self.processing:
            return
            
        self.processing = True
        
        # Run capture in separate thread
        thread = threading.Thread(target=self._capture_and_process, args=(cursor_x, cursor_y))
        thread.daemon = True
        thread.start()
    
    def _capture_and_process(self, cursor_x, cursor_y):
        """Capture and process entire screen in background thread with GPU acceleration."""
        try:
            # Capture entire screen
            img = ImageGrab.grab()
            
            # Store the capture
            self.last_capture = {
                'image': img,
                'timestamp': time.time(),
                'cursor_pos': (cursor_x, cursor_y)
            }
            
            print(f"[SUCCESS] Captured entire screen - Image size: {img.size}")
            
            # GPU-accelerated preprocessing
            if CV2_AVAILABLE:
                print("Applying GPU-accelerated preprocessing...")
                img = self.gpu_processor.preprocess_image_gpu(img)
            
            # Extract text from the image
            self._process_text_extraction(img)
            
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Capture error: {error_msg}")
            self.ui.root.after(0, lambda: self.ui.update_status(f"Error: {error_msg}"))
        finally:
            self.processing = False
    
    def _process_text_extraction(self, img):
        """Process text extraction and update UI."""
        try:
            self.ui.root.after(0, lambda: self.ui.update_status("GPU-accelerated text extraction..."))
            
            # Extract text using GPU processor
            text_lines = self.gpu_processor.extract_text_gpu(img)
            
            # Display text on the overlay
            self.ui.root.after(0, lambda: self.display_text(text_lines))
            
            # Update status
            self.ui.root.after(0, lambda: self.ui.update_status(f"GPU: Found {len(text_lines)} text lines"))
            
            print(f"[COMPLETE] GPU OCR processing finished - starting next capture in 2 seconds")
            self.ui.root.after(0, lambda: self.ui.update_status("GPU OCR complete - next capture in 2s"))
            # Schedule next automatic capture in 2 seconds
            self.ui.root.after(2000, self.start_next_capture)
            
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] GPU OCR error: {error_msg}")
            self.ui.root.after(0, lambda: self.ui.update_status(f"GPU OCR Error: {error_msg}"))
            self.ui.root.after(0, lambda: self.display_text(["Error extracting text"]))
            
            print(f"[COMPLETE] GPU OCR processing finished - starting next capture in 2 seconds")
            self.ui.root.after(0, lambda: self.ui.update_status("GPU OCR complete - next capture in 2s"))
            # Schedule next automatic capture in 2 seconds even if OCR failed
            self.ui.root.after(2000, self.start_next_capture)
    
    def display_text(self, text_list):
        """Display extracted text on the overlay with adaptive sizing."""
        # Clear previous text
        self.ui.clear_text()
    
        # Add new text
        if text_list:
            display_text = "\n".join(text_list)
            print("[display_text]", display_text)
            self.ui.add_text(display_text)
            
            # Calculate required size based on text content
            new_width, new_height = self.ui.calculate_window_size(text_list)
            self.ui.resize_window(new_width, new_height)
        else:
            self.ui.add_text("No text found around cursor")
            # Reset to minimum size if no text
            self.ui.resize_window(self.ui.min_width, self.ui.min_height)
    
    def get_last_capture(self):
        """Get the last captured screen image."""
        return self.last_capture
    
    def stop_capture(self):
        """Stop the capture loop."""
        self.capturing = False
        self.processing = False 