"""
Cursor tracking functionality for the overlay window.
Handles window positioning and cursor following.
"""

from .imports import *

class CursorTracker:
    """Handles cursor tracking and window positioning."""
    
    def __init__(self, root, ui_components):
        self.root = root
        self.ui = ui_components
        self.tracking = True
        
    def start_tracking(self):
        """Start cursor tracking."""
        self.tracking = True
        self.track_cursor()
    
    def stop_tracking(self):
        """Stop cursor tracking."""
        self.tracking = False
    
    def track_cursor(self):
        """Track cursor position and move overlay window."""
        if not self.tracking:
            return
            
        try:
            # Get current mouse position
            x, y = pyautogui.position()
            
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Calculate new position (follow cursor with offset)
            new_x = x + 20  # 20 pixels to the right of cursor
            new_y = y - self.ui.window_height//2  # Center vertically on cursor
            
            # Keep window within screen bounds
            new_x = max(0, min(new_x, screen_width - self.ui.window_width))
            new_y = max(0, min(new_y, screen_height - self.ui.window_height))
            
            # Update window position
            self.root.geometry(f"{self.ui.window_width}x{self.ui.window_height}+{new_x}+{new_y}")
            
        except Exception as e:
            print(f"[ERROR] Cursor tracking error: {e}")
        
        # Schedule next update
        self.root.after(100, self.track_cursor)  # Update every 100ms
    
    def get_cursor_position(self):
        """Get current cursor position."""
        try:
            return pyautogui.position()
        except Exception as e:
            print(f"[ERROR] Failed to get cursor position: {e}")
            return (0, 0)
    
    def is_cursor_in_window(self):
        """Check if cursor is within the overlay window bounds."""
        try:
            cursor_x, cursor_y = pyautogui.position()
            window_x = self.root.winfo_x()
            window_y = self.root.winfo_y()
            
            return (window_x <= cursor_x <= window_x + self.ui.window_width and
                    window_y <= cursor_y <= window_y + self.ui.window_height)
        except Exception:
            return False 