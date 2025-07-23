"""
Main application class for AI-powered screenshot analysis.
Orchestrates all components and manages the application lifecycle.
"""

import tkinter as tk
import os
from .imports import *
from .openai_processor import OpenAIProcessor
from .ui_components import UIComponents
from .screen_capture import ScreenCapture
from .cursor_tracker import CursorTracker

class AIScreenshotAnalyzer:
    """Main application class for AI-powered screenshot analysis."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Initialize components
        self.openai_processor = OpenAIProcessor()
        self.ui = UIComponents(self.root, *DEFAULT_WINDOW_SIZE)
        self.cursor_tracker = CursorTracker(self.root, self.ui)
        self.screen_capture = ScreenCapture(self.openai_processor, self.ui)
        
        # Setup callbacks and bindings
        self.setup_callbacks()
        self.setup_bindings()
        
        # Update UI with AI status
        self.update_ai_status()
        
        # Start components
        self.cursor_tracker.start_tracking()
        
        # Auto-start capture after 3 seconds (longer for AI setup)
        self.root.after(3000, self.screen_capture.start_capture_loop)
    
    def setup_window(self):
        """Setup the main window properties."""
        self.root.title("AI Screenshot Analyzer")
        
        # Make the window transparent and always on top
        self.root.attributes('-alpha', 0.90)
        self.root.attributes('-topmost', True)
        
        # Remove window decorations
        self.root.overrideredirect(True)
    
    def setup_callbacks(self):
        """Setup UI callbacks."""
        self.ui.set_capture_callback(self.screen_capture.toggle_capture)
        self.ui.set_close_callback(self.root.destroy)
        self.ui.set_mode_change_callback(self.on_analysis_mode_change)
    
    def setup_bindings(self):
        """Setup keyboard bindings."""
        # Bind escape key to close
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # Bind Ctrl+A to toggle capture
        self.root.bind('<Control-a>', lambda e: self.screen_capture.toggle_capture())
        
        # Bind Ctrl+M to cycle analysis modes
        self.root.bind('<Control-m>', lambda e: self.ui.toggle_analysis_mode())
        
        # Bind Ctrl+P for custom prompt
        self.root.bind('<Control-p>', lambda e: self.custom_analysis_prompt())
    
    def on_analysis_mode_change(self, mode):
        """Handle analysis mode changes."""
        self.screen_capture.set_analysis_mode(mode)
        self.ui.update_status(f"Analysis mode: {mode.capitalize()}")
    
    def custom_analysis_prompt(self):
        """Handle custom analysis prompt."""
        prompt = self.ui.add_custom_prompt_dialog()
        if prompt:
            self.screen_capture.custom_analysis(prompt)
    
    def update_ai_status(self):
        """Update UI with current AI status."""
        ai_status = self.openai_processor.get_status()
        
        # Update AI status in UI
        if ai_status['api_available']:
            model_display = ai_status['model'].replace('-preview', '')
            self.ui.update_ai_label("Connected", model_display)
        else:
            self.ui.update_ai_label("Error", None)
        
        # Print status summary
        print("\n=== AI Status Summary ===")
        print(f"OpenAI API: {'✓' if ai_status['api_available'] else '✗'}")
        if ai_status['api_available']:
            print(f"Model: {ai_status['model']}")
            print(f"Models Accessible: {'✓' if ai_status.get('models_accessible', False) else '✗'}")
        else:
            print(f"Error: {ai_status.get('error', 'Unknown error')}")
        print("========================\n")
    
    def run(self):
        """Start the application main loop."""
        print("🤖 AI-Powered Screenshot Analyzer Started!")
        print("Controls:")
        print("  - ESC: Close application")
        print("  - Ctrl+A: Manual analysis")
        print("  - Ctrl+M: Change analysis mode")
        print("  - Ctrl+P: Custom analysis prompt")
        print("  - Click 'Analyze Now' button")
        print("  - Click 'Mode' button to cycle modes")
        print("  - Automatic analysis every 5 seconds")
        print()
        
        # Check for OpenAI API key
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  Warning: OPENAI_API_KEY environment variable not set!")
            print("   Please set your OpenAI API key as an environment variable.")
            print("   Example: export OPENAI_API_KEY='your-api-key-here'")
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
        app = AIScreenshotAnalyzer()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'app' in locals():
            app.cleanup()

if __name__ == "__main__":
    main() 