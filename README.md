# AI-Powered Screenshot Analyzer

An intelligent screenshot analysis tool powered by OpenAI's GPT-4 Vision API. This application captures screenshots and uses AI to provide insightful analysis, text extraction, UI descriptions, and content summaries.

## Quick Setup (You're Almost Ready!)

Since you've already added your `OPENAI_API_KEY`, you're almost ready to go! Just follow these final steps:

### 1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### 2. **Verify your setup**:
```bash
# Test basic installation
python setup_test.py

# Test vision functionality
python test_openai_vision.py
```

### 3. **Run the application**:
```bash
python run.py
```

## Features

- **AI-Powered Analysis**: Uses GPT-4 Vision to analyze screenshots intelligently
- **Multiple Analysis Modes**:
  - **General**: Overall analysis and insights
  - **Text**: Extract and organize visible text
  - **UI**: Describe interface elements and layout
  - **Summary**: Provide concise content summaries
- **Real-time Processing**: Automatic screenshot capture and analysis
- **Interactive Interface**: Clean, modern overlay window
- **Cursor Following**: Window follows your cursor for convenient access
- **Custom Prompts**: Define your own analysis prompts

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Windows 10/11 (tested platform)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cluecursor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**:
   ```bash
   # Windows
   set OPENAI_API_KEY=your-api-key-here
   
   # Linux/Mac
   export OPENAI_API_KEY=your-api-key-here
   ```

## Usage

### Running the Application

```bash
python run.py
```

### Controls

- **ESC**: Close application
- **Ctrl+A**: Manual screenshot analysis
- **Ctrl+M**: Cycle through analysis modes
- **Ctrl+P**: Custom analysis with your own prompt
- **Click "Analyze Now"**: Trigger immediate analysis
- **Click "Mode"**: Change analysis mode
- **Automatic**: Analysis runs every 5 seconds

### Analysis Modes

1. **General**: Comprehensive analysis focusing on main content, purpose, and notable patterns
2. **Text**: Extracts and organizes all visible text while preserving structure
3. **UI**: Describes interface elements, buttons, menus, and layout patterns
4. **Summary**: Provides concise summaries of key information and main topics

## Configuration

The application can be configured by modifying constants in `src/imports.py`:

- `DEFAULT_WINDOW_SIZE`: Initial window dimensions
- `MAX_TOKENS`: Maximum tokens for AI responses
- `TEMPERATURE`: AI response creativity (0.0-1.0)

## API Usage

The application uses OpenAI's GPT-4 Vision API. Ensure you have:
- Valid OpenAI API key
- Sufficient API credits
- Internet connection

## Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**:
   - Set the `OPENAI_API_KEY` environment variable
   - Restart your terminal/command prompt

2. **"OpenAI library not available"**:
   ```bash
   pip install openai
   ```

3. **High API usage**:
   - Increase the analysis interval in `src/screen_capture.py`
   - Use manual mode instead of automatic

### Performance Tips

- Use specific analysis modes for better performance
- Adjust window size for optimal text display
- Use custom prompts for targeted analysis

## Development

### Project Structure

```
cluecursor/
├── src/
│   ├── main_app.py          # Main application orchestrator
│   ├── openai_processor.py  # OpenAI API integration
│   ├── screen_capture.py    # Screenshot capture and analysis
│   ├── ui_components.py     # User interface components
│   ├── cursor_tracker.py    # Cursor tracking functionality
│   └── imports.py           # Import management
├── requirements.txt         # Python dependencies
├── run.py                  # Application entry point
└── README.md               # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Acknowledgments

- OpenAI for the GPT-4 Vision API
- Python community for excellent libraries
- Contributors and users

---

**Note**: This application requires an active internet connection and valid OpenAI API credentials to function properly.
