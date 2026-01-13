"""Configuration settings for the PowerPoint generator."""

import os

# DeepSeek API Configuration
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', 'sk-ee23ea3fdaab41e799aeb2d12aacf67c')
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# Supported file extensions for reading
SUPPORTED_EXTENSIONS = {
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
