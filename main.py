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
    print("pytesseract available")
except ImportError:
    OCR_AVAILABLE = False
    print("pytesseract not available")

try:
    import easyocr
    EASYOCR_AVAILABLE = True
    print("easyocr available")
except ImportError:
    EASYOCR_AVAILABLE = False
    print("easyocr not available")

class ScreenCaptureOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Capture Overlay")
        
        # Make the window transparent
        self.root.attributes('-alpha', 0.85)  # 85% transparency for better text visibility
        self.root.attributes('-topmost', True)  # Keep on top
        
        # Set initial window size and position
        self.window_width = 350
        self.window_height = 450
        self.min_width = 300
        self.min_height = 200
        self.max_width = 800
        self.max_height = 1000
        
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Create a canvas for drawing
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height, 
                               bg='gray', highlightthickness=0)
        self.canvas.pack()
        
        # Draw a gray background
        self.canvas.create_rectangle(0, 0, self.window_width, self.window_height, 
                                   fill='gray', outline='white', width=2)
        
        # Add title
        self.title_label = tk.Label(self.root, text="Cursor Text Reader", 
                                   bg='gray', fg='white', font=('Arial', 12, 'bold'))
        self.title_label.place(x=self.window_width//2-60, y=5)
        
        # Add capture button
        self.capture_button = tk.Button(self.root, text="📷 Manual Capture", command=self.toggle_capture,
                                       bg='darkgray', fg='white', font=('Arial', 12, 'bold'),
                                       width=15, height=1)
        self.capture_button.place(x=self.window_width//2-60, y=30)
        
        # Add close button
        self.close_button = tk.Button(self.root, text="X", command=self.root.destroy,
                                     bg='darkgray', fg='white', font=('Arial', 10, 'bold'))
        self.close_button.place(x=self.window_width-25, y=5)
        
        # Bind escape key to close
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # Bind Ctrl+C to toggle capture
        self.root.bind('<Control-c>', lambda e: self.toggle_capture())
        
        # Screen capture setup
        self.last_capture = None
        self.processing = False
        self.capturing = False
        
        # Text display area with scrollbar
        self.text_frame = tk.Frame(self.root, bg='gray')
        self.text_frame.place(x=10, y=70, width=self.window_width-20, height=self.window_height-120)
        
        self.text_area = tk.Text(self.text_frame, bg='lightgray', fg='black', 
                                font=('Consolas', 9), wrap=tk.WORD)
        self.scrollbar = tk.Scrollbar(self.text_frame, orient="vertical", command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)
        
        self.text_area.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Status label
        self.status_label = tk.Label(self.root, text="Starting automatic capture in 2s...", 
                                    bg='gray', fg='white', font=('Arial', 9))
        self.status_label.place(x=10, y=self.window_height-30)
        
        # OCR method indicator
        ocr_method = "pytesseract" if OCR_AVAILABLE else "easyocr" if EASYOCR_AVAILABLE else "None"
        self.ocr_label = tk.Label(self.root, text=f"OCR: {ocr_method}", 
                                 bg='gray', fg='yellow', font=('Arial', 8))
        self.ocr_label.place(x=self.window_width-80, y=self.window_height-30)
        
        print("Screen capture overlay ready!")
        if not OCR_AVAILABLE and not EASYOCR_AVAILABLE:
            print("WARNING: No OCR library available. Install pytesseract or easyocr.")
        else:
            print("OCR libraries detected. Testing setup...")
            if EASYOCR_AVAILABLE:
                try:
                    import numpy as np
                    print("numpy available for EasyOCR")
                except ImportError:
                    print("WARNING: Install numpy for EasyOCR: pip install numpy")
            if OCR_AVAILABLE:
                try:
                    import pytesseract
                    # Set the path to your Tesseract installation
                    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                    # Test if tesseract is installed
                    pytesseract.get_tesseract_version()
                    print("Tesseract OCR engine found and working")
                except Exception as e:
                    print(f"WARNING: Tesseract not working: {e}")
                    print("Make sure Tesseract is installed at: C:\\Program Files\\Tesseract-OCR")
        
        # Start cursor tracking
        self.track_cursor()
        
        # Auto-start capture after 2 seconds
        self.root.after(2000, self.auto_start_capture)
    
    def auto_start_capture(self):
        """Automatically start capture mode"""
        self.capturing = True
        self.status_label.config(text="Starting automatic capture...")
        print("Started automatic capture mode")
        # Start the first capture after 2 seconds
        self.root.after(2000, self.start_next_capture)
    
    def toggle_capture(self):
        """Manual trigger for screen capture"""
        if not self.processing:
            # Get current cursor position
            x, y = pyautogui.position()
            print(f"\n[MANUAL] Manual capture triggered at cursor position ({x}, {y}) - {time.strftime('%H:%M:%S')}")
            self.capture_around_cursor(x, y)
        else:
            print(f"[BUSY] Still processing previous capture - {time.strftime('%H:%M:%S')}")
    
    def start_next_capture(self):
        """Start the next automatic capture"""
        if self.capturing and not self.processing:
            # Get current cursor position
            x, y = pyautogui.position()
            print(f"\n[AUTO] Starting automatic full screen capture at cursor position ({x}, {y}) - {time.strftime('%H:%M:%S')}")
            self.capture_around_cursor(x, y)
        elif self.processing:
            print(f"[WAIT] Still processing - will retry in 2 seconds - {time.strftime('%H:%M:%S')}")
            # Retry in 2 seconds if still processing
            self.root.after(2000, self.start_next_capture)
    
    def periodic_capture(self):
        """Legacy function - no longer used"""
        pass
    
    def schedule_next_capture(self):
        """Legacy function - no longer used"""
        pass
    
    def track_cursor(self):
        """Track cursor position and move overlay"""
        try:
            # Get current mouse position
            x, y = pyautogui.position()
            
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Calculate new position (follow cursor with offset)
            new_x = x + 20  # 20 pixels to the right of cursor
            new_y = y - self.window_height//2  # Center vertically on cursor
            
            # Keep window within screen bounds
            new_x = max(0, min(new_x, screen_width - self.window_width))
            new_y = max(0, min(new_y, screen_height - self.window_height))
            
            # Update window position
            self.root.geometry(f"{self.window_width}x{self.window_height}+{new_x}+{new_y}")
            
            # Capture area around cursor if capturing is enabled (now handled by periodic_capture)
            # Removed automatic capture from cursor tracking to avoid conflicts
            
        except Exception as e:
            print(f"[ERROR] Cursor tracking error: {e}")
        
        # Schedule next update
        self.root.after(100, self.track_cursor)  # Update every 100ms
    
    def capture_around_cursor(self, cursor_x, cursor_y):
        """Capture area around cursor and extract text"""
        if self.processing:
            return
            
        self.processing = True
        
        # Run capture in separate thread
        thread = threading.Thread(target=self._capture_and_process, args=(cursor_x, cursor_y))
        thread.daemon = True
        thread.start()
    
    def _capture_and_process(self, cursor_x, cursor_y):
        """Capture and process entire screen in background thread"""
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
            
            # Extract text from the image
            self.extract_text(img)
            
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Capture error: {error_msg}")
            self.root.after(0, lambda: self.status_label.config(text=f"Error: {error_msg}"))
        finally:
            self.processing = False
    
    def extract_text(self, img):
        """Extract text from the captured image using available OCR"""
        try:
            self.root.after(0, lambda: self.status_label.config(text="Extracting text..."))
            
            print("Extracting text from image...")
            
            text = ""
            
            # Try pytesseract first (faster)
            if OCR_AVAILABLE:
                try:
                    text = pytesseract.image_to_string(img)
                    print("Used pytesseract for OCR")
                except Exception as e:
                    print(f"pytesseract failed: {e}")
                    text = ""
            
            # Fallback to easyocr if pytesseract failed or unavailable
            if not text and EASYOCR_AVAILABLE:
                try:
                    import numpy as np
                    # Convert PIL Image to numpy array for easyocr
                    img_array = np.array(img)
                    reader = easyocr.Reader(['en'])
                    results = reader.readtext(img_array)
                    text_lines = []
                    for (bbox, detected_text, prob) in results:
                        if prob > 0.5:  # Only include high confidence text
                            text_lines.append(detected_text)
                    text = "\n".join(text_lines)
                    print("Used easyocr for OCR")
                except Exception as e:
                    print(f"easyocr failed: {e}")
                    text = ""
            
            # Clean up the text
            lines = text.strip().split('\n')
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            
            # If no OCR worked, show a message
            if not cleaned_lines:
                cleaned_lines = ["No text detected - OCR libraries may need setup"]
                print("[INFO] No text found - consider installing Tesseract OCR")
            
            # Display text on the overlay
            self.root.after(0, lambda: self.display_text(cleaned_lines))
            
            print(f"[TEXT] Found {len(cleaned_lines)} text lines")
            if cleaned_lines:
                print(f"[TEXT] Sample text: {cleaned_lines[0][:50]}{'...' if len(cleaned_lines[0]) > 50 else ''}")
            self.root.after(0, lambda: self.status_label.config(text=f"Found {len(cleaned_lines)} text lines"))
            
            print(f"[COMPLETE] OCR processing finished - starting next capture in 2 seconds")
            self.root.after(0, lambda: self.status_label.config(text="OCR complete - next capture in 2s"))
            # Schedule next automatic capture in 2 seconds
            self.root.after(2000, self.start_next_capture)
            
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] OCR error: {error_msg}")
            self.root.after(0, lambda: self.status_label.config(text=f"OCR Error: {error_msg}"))
            self.root.after(0, lambda: self.display_text(["Error extracting text"]))
            
            print(f"[COMPLETE] OCR processing finished - starting next capture in 2 seconds")
            self.root.after(0, lambda: self.status_label.config(text="OCR complete - next capture in 2s"))
            # Schedule next automatic capture in 2 seconds even if OCR failed
            self.root.after(2000, self.start_next_capture)
    
    def display_text(self, text_list):
        """Display extracted text on the overlay with adaptive sizing"""
        # Clear previous text
        self.text_area.delete(1.0, tk.END)
    
        # Add new text
        if text_list:
            display_text = "\n".join(text_list)
            print("[display_text]", display_text)
            self.text_area.insert(tk.END, display_text)
            
            # Calculate required size based on text content
            self.resize_window_for_text(text_list)
        else:
            self.text_area.insert(tk.END, "No text found around cursor")
            # Reset to minimum size if no text
            self.resize_window(300, 200)
    
    def resize_window_for_text(self, text_list):
        """Resize window based on text content"""
        if not text_list:
            return
            
        # Calculate text dimensions
        total_lines = len(text_list)
        max_line_length = max(len(line) for line in text_list) if text_list else 0
        
        # Estimate required dimensions
        # Each line is approximately 9 pixels high (font size)
        # Each character is approximately 6 pixels wide (Consolas font)
        estimated_height = total_lines * 12 + 120  # 120 for UI elements
        estimated_width = max_line_length * 7 + 40  # 40 for margins and scrollbar
        
        # Apply constraints
        new_width = max(self.min_width, min(self.max_width, estimated_width))
        new_height = max(self.min_height, min(self.max_height, estimated_height))
        
        # Resize the window
        self.resize_window(new_width, new_height)
    
    def resize_window(self, new_width, new_height):
        """Resize the window and reposition all elements"""
        # Get current position
        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()
        
        # Update window size
        self.window_width = new_width
        self.window_height = new_height
        
        # Resize the window
        self.root.geometry(f"{new_width}x{new_height}+{current_x}+{current_y}")
        
        # Update canvas
        self.canvas.config(width=new_width, height=new_height)
        self.canvas.delete("all")  # Clear canvas
        self.canvas.create_rectangle(0, 0, new_width, new_height, 
                                   fill='gray', outline='white', width=2)
        
        # Reposition title
        self.title_label.place(x=new_width//2-60, y=5)
        
        # Reposition capture button
        self.capture_button.place(x=new_width//2-60, y=30)
        
        # Reposition close button
        self.close_button.place(x=new_width-25, y=5)
        
        # Resize and reposition text frame
        self.text_frame.place(x=10, y=70, width=new_width-20, height=new_height-120)
        
        # Reposition status label
        self.status_label.place(x=10, y=new_height-30)
        
        # Reposition OCR label
        self.ocr_label.place(x=new_width-80, y=new_height-30)
        
        print(f"[RESIZE] Window resized to {new_width}x{new_height} for {len(text_list) if 'text_list' in locals() else 0} lines of text")
    
    def get_last_capture(self):
        """Get the last captured screen image"""
        return self.last_capture
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Disable pyautogui failsafe
    pyautogui.FAILSAFE = False
    
    overlay = ScreenCaptureOverlay()
    overlay.run()