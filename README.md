# 🎯 AI PowerPoint Generator

> Transform any document into stunning presentations using AI (DeepSeek LLM)

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 📄 **Multi-format Support** - Read content from TXT, MD, PDF, DOCX, CSV, JSON, XML, HTML, and Python files
- 🤖 **AI-Powered** - Uses DeepSeek LLM to intelligently analyze content and create structured presentations
- 🎨 **Multiple Themes** - Choose from 6 professional themes: Professional, Modern, Creative, Corporate, Minimal, Vibrant
- 📊 **Professional Output** - Generates polished PPTX files with proper styling, speaker notes, and consistent formatting
- 🖥️ **Rich CLI** - Beautiful terminal interface with progress bars, colors, and interactive mode
- ⚡ **Smart & Fast** - Automatic retry logic, error handling, and optimized content processing

## 🚀 Installation

```bash
# Clone or download the project
cd p10

# Install dependencies
uv sync
```

## 📖 Usage

### Quick Start

```bash
# Basic usage - creates presentation from input file
uv run python main.py document.pdf

# Specify custom output filename
uv run python main.py document.pdf my-presentation.pptx

# Use a specific theme
uv run python main.py notes.txt --theme modern
```

### Interactive Mode

For a guided experience with prompts:

```bash
uv run python main.py --interactive
```

### Command Line Options

```
Usage: pptgen [OPTIONS] INPUT_FILE [OUTPUT_FILE]

Arguments:
  INPUT_FILE    Input file to convert (PDF, DOCX, TXT, MD, etc.)
  OUTPUT_FILE   Output PPTX file (default: input filename with .pptx)

Options:
  -t, --theme     Presentation theme (professional, modern, creative, 
                  corporate, minimal, vibrant)
  -i, --interactive  Run in interactive mode with prompts
  --formats       Show supported file formats
  --themes        Show available presentation themes
  -q, --quiet     Minimal output (no banner/progress)
  -v, --version   Show version number
  -h, --help      Show help message
```

### Examples

```bash
# From a PDF document with modern theme
uv run python main.py report.pdf output.pptx --theme modern

# From a Markdown file
uv run python main.py README.md

# From CSV data with creative theme
uv run python main.py data.csv analysis.pptx --theme creative

# View all supported formats
uv run python main.py --formats

# View all themes
uv run python main.py --themes
```

## 🎨 Available Themes

| Theme | Style | Best For |
|-------|-------|----------|
| **Professional** | Clean & Business | Corporate presentations, reports |
| **Modern** | Sleek & Contemporary | Tech demos, startups |
| **Creative** | Bold & Expressive | Marketing, design showcases |
| **Corporate** | Formal & Traditional | Executive meetings, finance |
| **Minimal** | Simple & Elegant | Academic, research presentations |
| **Vibrant** | Colorful & Energetic | Training, workshops |

## 📄 Supported File Types

| Extension | Type | Description |
|-----------|------|-------------|
| `.txt` | Text | Plain text documents |
| `.md` | Markdown | Markdown documentation |
| `.pdf` | PDF | PDF documents (text extraction) |
| `.docx` | Word | Microsoft Word documents |
| `.csv` | CSV | Spreadsheet/tabular data |
| `.json` | JSON | JSON data files |
| `.xml` | XML | XML markup files |
| `.html` | HTML | Web pages |
| `.py` | Python | Python source code |

## 📁 Project Structure

```
├── main.py           # Entry point with CLI interface
├── config.py         # Configuration (themes, settings, API)
├── file_reader.py    # Multi-format file reading
├── llm_client.py     # DeepSeek LLM integration
├── pptx_generator.py # PowerPoint generation with themes
├── pyproject.toml    # Project dependencies
└── README.md         # Documentation
```

## ⚙️ Configuration

### API Key

Set your DeepSeek API key via environment variable:

```bash
# Windows
set DEEPSEEK_API_KEY=your-api-key

# Linux/Mac
export DEEPSEEK_API_KEY=your-api-key
```

Or modify `config.py` directly.

### Customization

Edit `config.py` to customize:

- **Themes** - Add or modify color schemes and fonts
- **LLM Settings** - Adjust token limits, retry logic
- **File Limits** - Change maximum file size

## 🔧 Requirements

- Python 3.13+
- DeepSeek API key
- Dependencies (auto-installed):
  - `openai` - LLM API client
  - `python-pptx` - PowerPoint generation
  - `pypdf` - PDF reading
  - `python-docx` - Word document reading
  - `rich` - Beautiful CLI interface

## 📝 How It Works

1. **📖 Read** - The tool reads your input file and extracts text content
2. **🤖 Analyze** - AI analyzes the content and creates a logical presentation structure
3. **🎨 Generate** - Creates a professional PPTX with your chosen theme
4. **✨ Output** - Saves the final presentation with proper formatting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

MIT License - feel free to use this project for any purpose.

---

Made with ❤️ using DeepSeek AI and Python
