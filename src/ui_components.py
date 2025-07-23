"""
UI components and window management for the AI-powered screenshot analysis overlay.
Handles window creation, styling, user interface elements, and analysis mode controls.
"""

from .imports import *

class UIComponents:
    """Manages UI components and window styling for AI analysis."""
    
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
        self.mode_button = None
        self.close_button = None
        self.text_frame = None
        self.text_area = None
        self.scrollbar = None
        self.status_label = None
        self.ai_label = None
        
        # Analysis mode tracking
        self.analysis_modes = ["General", "Text", "UI", "Summary"]
        self.current_mode_index = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI components."""
        # Create canvas for drawing
        self.canvas = tk.Canvas(
            self.root, 
            width=self.window_width, 
            height=self.window_height, 
            bg='darkslategray', 
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Draw background
        self.canvas.create_rectangle(
            0, 0, self.window_width, self.window_height, 
            fill='darkslategray', outline='lightblue', width=2
        )
        
        # Create title
        self.title_label = tk.Label(
            self.root, 
            text="🤖 AI Screenshot Analyzer", 
            bg='darkslategray', 
            fg='lightblue', 
            font=('Arial', 12, 'bold')
        )
        self.title_label.place(x=self.window_width//2-90, y=5)
        
        # Create capture button
        self.capture_button = tk.Button(
            self.root, 
            text="📸 Analyze Now", 
            bg='slategray', 
            fg='lightblue', 
            font=('Arial', 10, 'bold'),
            width=12, 
            height=1
        )
        self.capture_button.place(x=10, y=30)
        
        # Create mode toggle button
        self.mode_button = tk.Button(
            self.root, 
            text="Mode: General", 
            bg='slategray', 
            fg='lightgreen', 
            font=('Arial', 10, 'bold'),
            width=12, 
            height=1,
            command=self.toggle_analysis_mode
        )
        self.mode_button.place(x=130, y=30)
        
        # Create close button
        self.close_button = tk.Button(
            self.root, 
            text="✕", 
            bg='slategray', 
            fg='lightcoral', 
            font=('Arial', 10, 'bold'),
            width=3
        )
        self.close_button.place(x=self.window_width-35, y=5)
        
        # Create text display area
        self.setup_text_area()
        
        # Create status labels
        self.setup_status_labels()
    
    def setup_text_area(self):
        """Setup the text display area with scrollbar for AI responses."""
        self.text_frame = tk.Frame(self.root, bg='darkslategray')
        self.text_frame.place(
            x=10, y=70, 
            width=self.window_width-20, 
            height=self.window_height-120
        )
        
        self.text_area = tk.Text(
            self.text_frame, 
            bg='black', 
            fg='lightgreen', 
            font=('Consolas', 9), 
            wrap=tk.WORD,
            insertbackground='lightgreen'
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
            text="Starting AI analysis in 2s...", 
            bg='darkslategray', 
            fg='lightyellow', 
            font=('Arial', 9)
        )
        self.status_label.place(x=10, y=self.window_height-30)
        
        # AI status indicator will be set later
        self.ai_label = tk.Label(
            self.root, 
            text="AI: Initializing...", 
            bg='darkslategray', 
            fg='lightgreen', 
            font=('Arial', 8)
        )
        self.ai_label.place(x=self.window_width-120, y=self.window_height-30)
    
    def toggle_analysis_mode(self):
        """Toggle between different analysis modes."""
        self.current_mode_index = (self.current_mode_index + 1) % len(self.analysis_modes)
        current_mode = self.analysis_modes[self.current_mode_index]
        self.mode_button.config(text=f"Mode: {current_mode}")
        
        # Trigger callback if set
        if hasattr(self, 'mode_change_callback'):
            self.mode_change_callback(current_mode.lower())
    
    def get_current_analysis_mode(self):
        """Get the current analysis mode."""
        return self.analysis_modes[self.current_mode_index].lower()
    
    def set_mode_change_callback(self, callback):
        """Set callback for when analysis mode changes."""
        self.mode_change_callback = callback
    
    def update_ai_label(self, status, model_name=None):
        """Update the AI status indicator."""
        if model_name:
            self.ai_label.config(text=f"AI: {model_name}")
        else:
            self.ai_label.config(text=f"AI: {status}")
    
    def update_status(self, message):
        """Update the status label."""
        self.status_label.config(text=message)
    
    def clear_text(self):
        """Clear the text display area."""
        self.text_area.delete(1.0, tk.END)
    
    def add_text(self, text):
        """Add text to the display area with better formatting for AI responses."""
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        header = f"=== AI Analysis ({timestamp}) ===\n"
        
        self.text_area.insert(tk.END, header)
        self.text_area.insert(tk.END, text)
        self.text_area.insert(tk.END, "\n\n" + "="*40 + "\n\n")
        
        # Auto-scroll to bottom
        self.text_area.see(tk.END)
    
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
            fill='darkslategray', outline='lightblue', width=2
        )
        
        # Reposition all elements
        self.title_label.place(x=new_width//2-90, y=5)
        self.capture_button.place(x=10, y=30)
        self.mode_button.place(x=130, y=30)
        self.close_button.place(x=new_width-35, y=5)
        self.text_frame.place(
            x=10, y=70, 
            width=new_width-20, 
            height=new_height-120
        )
        self.status_label.place(x=10, y=new_height-30)
        self.ai_label.place(x=new_width-120, y=new_height-30)
        
        print(f"[RESIZE] AI window resized to {new_width}x{new_height}")
    
    def calculate_window_size(self, text_lines):
        """Calculate optimal window size based on AI response content."""
        if not text_lines:
            return self.min_width, self.min_height
        
        # Calculate text dimensions
        total_lines = len(text_lines)
        max_line_length = max(len(line) for line in text_lines) if text_lines else 0
        
        # Estimate required dimensions (more generous for AI responses)
        estimated_height = total_lines * 15 + 140  # More space for formatted AI responses
        estimated_width = min(max_line_length * 8 + 60, 600)  # Cap width for readability
        
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
    
    def add_custom_prompt_dialog(self):
        """Show dialog for custom AI analysis prompt."""
        import tkinter.simpledialog as simpledialog
        
        prompt = simpledialog.askstring(
            "Custom AI Analysis",
            "Enter your custom analysis prompt:",
            initialvalue="Analyze this screenshot and tell me..."
        )
        
        return prompt 