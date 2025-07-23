"""
Screen capture functionality for AI-powered screenshot analysis.
Handles screen grabbing, cursor tracking, and OpenAI analysis scheduling.
"""

import threading
import time
from .imports import *

class ScreenCapture:
    """Handles screen capture and OpenAI analysis operations."""
    
    def __init__(self, openai_processor, ui_components):
        self.openai_processor = openai_processor
        self.ui = ui_components
        self.last_capture = None
        self.processing = False
        self.capturing = False
        self.analysis_mode = "general"  # general, text, ui, summary, custom
        
    def set_analysis_mode(self, mode):
        """Set the analysis mode for OpenAI processing."""
        self.analysis_mode = mode
        print(f"[MODE] Analysis mode set to: {mode}")
    
    def start_capture_loop(self):
        """Start the automatic capture loop."""
        self.capturing = True
        self.ui.update_status("Starting AI-powered screenshot analysis...")
        print("Started AI-powered automatic capture mode")
        # Start the first capture after 2 seconds
        self.ui.root.after(2000, self.start_next_capture)
    
    def toggle_capture(self):
        """Manual trigger for screen capture."""
        if not self.processing:
            # Get current cursor position
            x, y = pyautogui.position()
            print(f"\n[MANUAL] Manual AI analysis triggered at cursor position ({x}, {y}) - {time.strftime('%H:%M:%S')}")
            self.capture_and_analyze(x, y)
        else:
            print(f"[BUSY] Still processing previous capture - {time.strftime('%H:%M:%S')}")
    
    def start_next_capture(self):
        """Start the next automatic capture."""
        if self.capturing and not self.processing:
            # Get current cursor position
            x, y = pyautogui.position()
            print(f"\n[AUTO] Starting AI analysis at cursor position ({x}, {y}) - {time.strftime('%H:%M:%S')}")
            self.capture_and_analyze(x, y)
        elif self.processing:
            print(f"[WAIT] Still processing - will retry in 5 seconds - {time.strftime('%H:%M:%S')}")
            # Retry in 5 seconds if still processing (longer for AI analysis)
            self.ui.root.after(5000, self.start_next_capture)
    
    def capture_and_analyze(self, cursor_x, cursor_y):
        """Capture area around cursor and analyze with AI."""
        if self.processing:
            return
            
        self.processing = True
        
        # Run capture in separate thread
        thread = threading.Thread(target=self._capture_and_process, args=(cursor_x, cursor_y))
        thread.daemon = True
        thread.start()
    
    def _capture_and_process(self, cursor_x, cursor_y):
        """Capture and process entire screen in background thread with AI analysis."""
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
            
            # AI-powered analysis
            self._process_ai_analysis(img)
            
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Capture error: {error_msg}")
            self.ui.root.after(0, lambda: self.ui.update_status(f"Error: {error_msg}"))
        finally:
            self.processing = False
    
    def _process_ai_analysis(self, img):
        """Process AI analysis and update UI."""
        try:
            self.ui.root.after(0, lambda: self.ui.update_status("AI analyzing screenshot..."))
            
            # Analyze screenshot based on current mode
            if self.analysis_mode == "text":
                response = self.openai_processor.extract_text(img)
            elif self.analysis_mode == "ui":
                response = self.openai_processor.describe_ui(img)
            elif self.analysis_mode == "summary":
                response = self.openai_processor.summarize_content(img)
            else:  # general
                response = self.openai_processor.analyze_screenshot(img)
            
            # Display AI response on the overlay
            self.ui.root.after(0, lambda: self.display_analysis(response))
            
            # Update status
            analysis_type = self.analysis_mode.capitalize()
            self.ui.root.after(0, lambda: self.ui.update_status(f"AI {analysis_type} analysis complete"))
            
            print(f"[COMPLETE] AI analysis finished - starting next capture in 5 seconds")
            
            # Schedule next automatic capture in 5 seconds (longer for AI processing)
            self.ui.root.after(5000, self.start_next_capture)
            
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] AI analysis error: {error_msg}")
            self.ui.root.after(0, lambda: self.ui.update_status(f"AI Error: {error_msg}"))
            self.ui.root.after(0, lambda: self.display_analysis(f"Error: {error_msg}"))
            
            print(f"[COMPLETE] AI analysis finished - starting next capture in 5 seconds")
            # Schedule next automatic capture in 5 seconds even if analysis failed
            self.ui.root.after(5000, self.start_next_capture)
    
    def display_analysis(self, analysis_text):
        """Display AI analysis on the overlay with adaptive sizing."""
        # Clear previous text
        self.ui.clear_text()
    
        # Add new analysis
        if analysis_text:
            print("[AI Analysis]", analysis_text[:200] + "..." if len(analysis_text) > 200 else analysis_text)
            self.ui.add_text(analysis_text)
            
            # Calculate required size based on text content
            text_lines = analysis_text.split('\n')
            new_width, new_height = self.ui.calculate_window_size(text_lines)
            self.ui.resize_window(new_width, new_height)
        else:
            self.ui.add_text("No analysis available")
            # Reset to minimum size if no text
            self.ui.resize_window(self.ui.min_width, self.ui.min_height)
    
    def custom_analysis(self, custom_prompt):
        """Perform custom analysis with user-provided prompt."""
        if self.last_capture and self.last_capture['image']:
            try:
                self.ui.update_status("Running custom AI analysis...")
                response = self.openai_processor.custom_analysis(self.last_capture['image'], custom_prompt)
                self.display_analysis(response)
                self.ui.update_status("Custom AI analysis complete")
            except Exception as e:
                error_msg = f"Custom analysis error: {str(e)}"
                self.ui.update_status(error_msg)
                self.display_analysis(error_msg)
        else:
            self.ui.update_status("No screenshot available for analysis")
    
    def get_last_capture(self):
        """Get the last captured screen image."""
        return self.last_capture
    
    def stop_capture(self):
        """Stop the capture loop."""
        self.capturing = False
        self.processing = False 