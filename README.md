# AI PowerPoint Generator

Generate professional PowerPoint presentations from any file using AI (DeepSeek LLM).

## Features

- 📄 **Multi-format Support**: Read content from TXT, MD, PDF, DOCX, CSV, JSON, XML, HTML, and Python files
- 🤖 **AI-Powered**: Uses DeepSeek LLM to analyze content and create structured presentations
- 📊 **Professional Output**: Generates PPTX files with proper slide layouts and speaker notes

## Installation

```bash
uv sync
```

## Usage

```bash
# Basic usage - creates output.pptx from input file
uv run python main.py <input_file>

# Specify custom output filename
uv run python main.py <input_file> <output_file.pptx>
```

### Examples

```bash
# From a text file
uv run python main.py notes.txt

# From a PDF document
uv run python main.py document.pdf presentation.pptx

# From a CSV file
uv run python main.py data.csv

# From a Word document
uv run python main.py report.docx
```

## Project Structure

```
├── main.py           # Entry point - orchestrates the workflow
├── config.py         # Configuration settings (API keys, supported formats)
├── file_reader.py    # Reads content from various file types
├── llm_client.py     # Interacts with DeepSeek LLM API
├── pptx_generator.py # Creates PowerPoint presentations
└── pyproject.toml    # Project dependencies
```

## Configuration

The DeepSeek API key is configured in `config.py`. You can also set it via environment variable:

```bash
set DEEPSEEK_API_KEY=your-api-key
```

## Supported File Types

| Extension | Description |
|-----------|-------------|
| `.txt`    | Plain text files |
| `.md`     | Markdown files |
| `.pdf`    | PDF documents |
| `.docx`   | Word documents |
| `.csv`    | CSV data files |
| `.json`   | JSON files |
| `.xml`    | XML files |
| `.html`   | HTML files |
| `.py`     | Python source files |
