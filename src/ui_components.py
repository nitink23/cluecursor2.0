"""
UI components and window management for the GPU-optimized OCR overlay.
Handles window creation, styling, and user interface elements.
"""

from .imports import *

class UIComponents:
    """Manages UI components and window styling."""
    
    def __init__(self, root, window_width, window_height):
        self.root = root
        self.window_width = window_width
        self.window_height = window_height
        self.min_width, self.min_height = MIN_WINDOW_SIZE
        self.max_width, self.max_height = MAX_WINDOW_SIZE
        
        # Create UI components
        self.canvas = None
        self.title_label = None
        self.capture_button = None
        self.close_button = None
        self.text_frame = None
        self.text_area = None
        self.scrollbar = None
        self.status_label = None
        self.ocr_label = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI components."""
        # Create canvas for drawing
        self.canvas = tk.Canvas(
            self.root, 
            width=self.window_width, 
            height=self.window_height, 
            bg='darkblue', 
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Draw background
        self.canvas.create_rectangle(
            0, 0, self.window_width, self.window_height, 
            fill='darkblue', outline='cyan', width=2
        )
        
        # Create title
        self.title_label = tk.Label(
            self.root, 
            text="🚀 GPU Text Reader", 
            bg='darkblue', 
            fg='cyan', 
            font=('Arial', 12, 'bold')
        )
        self.title_label.place(x=self.window_width//2-70, y=5)
        
        # Create capture button
        self.capture_button = tk.Button(
            self.root, 
            text="📷 Manual Capture", 
            bg='navy', 
            fg='cyan', 
            font=('Arial', 12, 'bold'),
            width=15, 
            height=1
        )
        self.capture_button.place(x=self.window_width//2-60, y=30)
        
        # Create close button
        self.close_button = tk.Button(
            self.root, 
            text="X", 
            bg='navy', 
            fg='cyan', 
            font=('Arial', 10, 'bold')
        )
        self.close_button.place(x=self.window_width-25, y=5)
        
        # Create text display area
        self.setup_text_area()
        
        # Create status labels
        self.setup_status_labels()
    
    def setup_text_area(self):
        """Setup the text display area with scrollbar."""
        self.text_frame = tk.Frame(self.root, bg='darkblue')
        self.text_frame.place(
            x=10, y=70, 
            width=self.window_width-20, 
            height=self.window_height-120
        )
        
        self.text_area = tk.Text(
            self.text_frame, 
            bg='black', 
            fg='lime', 
            font=('Consolas', 9), 
            wrap=tk.WORD
        )
        self.scrollbar = tk.Scrollbar(
            self.text_frame, 
            orient="vertical", 
            command=self.text_area.yview
        )
        self.text_area.configure(yscrollcommand=self.scrollbar.set)
        
        self.text_area.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
    
    def setup_status_labels(self):
        """Setup status and information labels."""
        self.status_label = tk.Label(
            self.root, 
            text="Starting GPU-optimized capture in 2s...", 
            bg='darkblue', 
            fg='yellow', 
            font=('Arial', 9)
        )
        self.status_label.place(x=10, y=self.window_height-30)
        
        # OCR method indicator will be set later
        self.ocr_label = tk.Label(
            self.root, 
            text="GPU: Initializing...", 
            bg='darkblue', 
            fg='lime', 
            font=('Arial', 8)
        )
        self.ocr_label.place(x=self.window_width-100, y=self.window_height-30)
    
    def update_ocr_label(self, gpu_status, ocr_method):
        """Update the OCR method indicator."""
        self.ocr_label.config(text=f"{gpu_status}: {ocr_method}")
    
    def update_status(self, message):
        """Update the status label."""
        self.status_label.config(text=message)
    
    def clear_text(self):
        """Clear the text display area."""
        self.text_area.delete(1.0, tk.END)
    
    def add_text(self, text):
        """Add text to the display area."""
        self.text_area.insert(tk.END, text)
    
    def resize_window(self, new_width, new_height):
        """Resize the window and reposition all elements."""
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
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            0, 0, new_width, new_height, 
            fill='darkblue', outline='cyan', width=2
        )
        
        # Reposition all elements
        self.title_label.place(x=new_width//2-70, y=5)
        self.capture_button.place(x=new_width//2-60, y=30)
        self.close_button.place(x=new_width-25, y=5)
        self.text_frame.place(
            x=10, y=70, 
            width=new_width-20, 
            height=new_height-120
        )
        self.status_label.place(x=10, y=new_height-30)
        self.ocr_label.place(x=new_width-100, y=new_height-30)
        
        print(f"[RESIZE] GPU window resized to {new_width}x{new_height}")
    
    def calculate_window_size(self, text_list):
        """Calculate optimal window size based on text content."""
        if not text_list:
            return self.min_width, self.min_height
        
        # Calculate text dimensions
        total_lines = len(text_list)
        max_line_length = max(len(line) for line in text_list) if text_list else 0
        
        # Estimate required dimensions
        estimated_height = total_lines * 12 + 120  # 120 for UI elements
        estimated_width = max_line_length * 7 + 40  # 40 for margins and scrollbar
        
        # Apply constraints
        new_width = max(self.min_width, min(self.max_width, estimated_width))
        new_height = max(self.min_height, min(self.max_height, estimated_height))
        
        return new_width, new_height
    
    def set_capture_callback(self, callback):
        """Set the callback for the capture button."""
        self.capture_button.config(command=callback)
    
    def set_close_callback(self, callback):
        """Set the callback for the close button."""
        self.close_button.config(command=callback) 