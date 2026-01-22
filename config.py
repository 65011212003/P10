"""Configuration settings for the PowerPoint generator."""

import os
from typing import Dict, Any

# Application metadata
APP_NAME = "AI PowerPoint Generator"
APP_VERSION = "2.0.0"

# DeepSeek API Configuration
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', 'sk-ee23ea3fdaab41e799aeb2d12aacf67c')
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# LLM Settings
MAX_TOKENS = 8192
MAX_INPUT_CHARS = 50000  # Maximum characters to send to LLM
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds

# File reading limits
MAX_FILE_SIZE_MB = 50  # Maximum file size in MB
CHUNK_SIZE = 8192  # Buffer size for reading large files

# Supported file extensions for reading
SUPPORTED_EXTENSIONS: Dict[str, str] = {
    '.txt': 'text',
    '.md': 'markdown',
    '.py': 'python',
    '.json': 'json',
    '.csv': 'csv',
    '.xml': 'xml',
    '.html': 'html',
    '.pdf': 'pdf',
    '.docx': 'docx',
}

# Color schemes for presentations (RGB tuples)
COLOR_SCHEMES = {
    'professional': {
        'primary': (0, 82, 147),      # Dark blue
        'secondary': (0, 120, 215),    # Bright blue
        'accent': (255, 128, 0),       # Orange
        'text': (51, 51, 51),          # Dark gray
        'background': (255, 255, 255), # White
    },
    'modern': {
        'primary': (26, 26, 26),       # Near black
        'secondary': (76, 76, 76),     # Dark gray
        'accent': (0, 200, 150),       # Teal
        'text': (51, 51, 51),          # Dark gray
        'background': (250, 250, 250), # Off white
    },
    'creative': {
        'primary': (156, 39, 176),     # Purple
        'secondary': (233, 30, 99),    # Pink
        'accent': (255, 193, 7),       # Amber
        'text': (33, 33, 33),          # Almost black
        'background': (255, 255, 255), # White
    },
    'corporate': {
        'primary': (0, 51, 102),       # Navy
        'secondary': (102, 153, 204),  # Light blue
        'accent': (204, 153, 0),       # Gold
        'text': (51, 51, 51),          # Dark gray
        'background': (255, 255, 255), # White
    },
    'minimal': {
        'primary': (50, 50, 50),       # Dark gray
        'secondary': (120, 120, 120),  # Medium gray
        'accent': (0, 150, 136),       # Teal
        'text': (33, 33, 33),          # Almost black
        'background': (255, 255, 255), # White
    },
    'vibrant': {
        'primary': (255, 87, 34),      # Deep orange
        'secondary': (63, 81, 181),    # Indigo
        'accent': (76, 175, 80),       # Green
        'text': (33, 33, 33),          # Almost black
        'background': (255, 255, 255), # White
    }
}

# Presentation themes with full configuration
THEMES: Dict[str, Dict[str, Any]] = {
    'professional': {
        'name': 'Professional',
        'style': 'Clean & Business',
        'primary_color': '#005293',
        'colors': COLOR_SCHEMES['professional'],
        'font_title': 'Calibri',
        'font_body': 'Calibri',
        'title_size': 44,
        'subtitle_size': 28,
        'body_size': 20,
        'bullet_size': 18,
    },
    'modern': {
        'name': 'Modern',
        'style': 'Sleek & Contemporary',
        'primary_color': '#1a1a1a',
        'colors': COLOR_SCHEMES['modern'],
        'font_title': 'Segoe UI',
        'font_body': 'Segoe UI Light',
        'title_size': 48,
        'subtitle_size': 24,
        'body_size': 20,
        'bullet_size': 18,
    },
    'creative': {
        'name': 'Creative',
        'style': 'Bold & Expressive',
        'primary_color': '#9c27b0',
        'colors': COLOR_SCHEMES['creative'],
        'font_title': 'Arial Black',
        'font_body': 'Arial',
        'title_size': 42,
        'subtitle_size': 26,
        'body_size': 20,
        'bullet_size': 18,
    },
    'corporate': {
        'name': 'Corporate',
        'style': 'Formal & Traditional',
        'primary_color': '#003366',
        'colors': COLOR_SCHEMES['corporate'],
        'font_title': 'Georgia',
        'font_body': 'Calibri',
        'title_size': 40,
        'subtitle_size': 24,
        'body_size': 18,
        'bullet_size': 16,
    },
    'minimal': {
        'name': 'Minimal',
        'style': 'Simple & Elegant',
        'primary_color': '#323232',
        'colors': COLOR_SCHEMES['minimal'],
        'font_title': 'Helvetica',
        'font_body': 'Helvetica',
        'title_size': 44,
        'subtitle_size': 22,
        'body_size': 18,
        'bullet_size': 16,
    },
    'vibrant': {
        'name': 'Vibrant',
        'style': 'Colorful & Energetic',
        'primary_color': '#ff5722',
        'colors': COLOR_SCHEMES['vibrant'],
        'font_title': 'Arial',
        'font_body': 'Arial',
        'title_size': 46,
        'subtitle_size': 26,
        'body_size': 20,
        'bullet_size': 18,
    },
}

# Slide layout configurations
SLIDE_LAYOUTS = {
    'title': 0,
    'title_content': 1,
    'section_header': 2,
    'two_content': 3,
    'comparison': 4,
    'title_only': 5,
    'blank': 6,
}

# Default presentation settings
DEFAULT_SLIDE_WIDTH = 13.333  # inches (16:9)
DEFAULT_SLIDE_HEIGHT = 7.5    # inches (16:9)
