# AI PowerPoint Generator v3.0.0 - New Features Guide

## 🎉 What's New in v3.0.0

### 1. **Multi-LLM Provider Support** 🤖
Choose from multiple AI providers:
- **DeepSeek** (default) - Cost-effective and powerful
- **OpenAI GPT-4** - Industry-leading performance  
- **Anthropic Claude** - Advanced reasoning capabilities
- **Ollama** - Local/private models

**Usage:**
```bash
# Use OpenAI GPT-4
python main.py document.pdf --provider openai

# Use Anthropic Claude
python main.py document.pdf --provider anthropic

# Use local Ollama
python main.py document.pdf --provider ollama

# See all providers
python main.py --providers
```

**Setup:**
- DeepSeek: `DEEPSEEK_API_KEY` environment variable
- OpenAI: `OPENAI_API_KEY` environment variable
- Anthropic: `ANTHROPIC_API_KEY` + install: `pip install anthropic`
- Ollama: Install Ollama locally from https://ollama.ai

---

### 2. **Batch Processing Mode** 📂
Process multiple files at once with a single command.

**Usage:**
```bash
# Process multiple files
python main.py file1.txt file2.pdf file3.docx --batch

# With custom theme
python main.py *.md --batch --theme modern

# With specific provider
python main.py docs/*.pdf --batch --provider openai
```

**Features:**
- Processes up to 50 files
- Individual progress tracking
- Automatic error handling
- Summary report at the end

---

### 3. **Export to Multiple Formats** 📤
Export your presentations beyond PowerPoint.

**Usage:**
```bash
# Export to PDF
python main.py document.pdf --export pdf

# Export to HTML5 (reveal.js)
python main.py document.pdf --export html

# Works with batch mode
python main.py *.md --batch --export pdf
```

**Export Formats:**
- **PDF**: Requires LibreOffice or PowerPoint
  - Install LibreOffice: https://www.libreoffice.org/download/
- **HTML**: Self-contained reveal.js presentation
  - No dependencies required
  - Interactive slideshow in browser

---

### 4. **Image Extraction & Embedding** 🖼️
Automatically extract and embed images from PDF and DOCX files.

**Features:**
- Extracts up to 20 images per file
- Filters out small icons/logos (min 100x100px)
- Supports: JPEG, PNG from PDF and DOCX
- Smart placement in slides

**Usage:**
```python
from image_extractor import extract_images

# Extract images from PDF
images = extract_images('document.pdf', max_images=10)

for img in images:
    print(f"Page {img.page_num}: {img.width}x{img.height}")
    img.save(f"extracted_{img.page_num}.png")
```

---

### 5. **Chart Generation** 📊
Generate professional charts from CSV/JSON data.

**Chart Types:**
- Bar charts
- Line charts  
- Pie charts
- Auto-detection based on data structure

**Usage:**
```python
from chart_generator import ChartGenerator

# Create bar chart
data = {
    'Series 1': [10, 20, 30],
    'Series 2': [15, 25, 35]
}
categories = ['Q1', 'Q2', 'Q3']

ChartGenerator.create_bar_chart(slide, data, categories, "Sales Data")
```

---

### 6. **Enhanced Content Features** ✨

#### **Code Syntax Highlighting**
Detect and display code with proper formatting.

```python
from content_enhancer import create_code_slide

code = '''
def hello_world():
    print("Hello, World!")
'''

create_code_slide(prs, "Python Example", code, language="python", theme=theme)
```

#### **Data Tables**
Beautiful formatted tables with headers and alternating row colors.

```python
from content_enhancer import create_table_slide

headers = ['Name', 'Value', 'Status']
rows = [
    ['Item 1', '100', 'Active'],
    ['Item 2', '200', 'Pending']
]

create_table_slide(prs, "Results", headers, rows, theme=theme)
```

#### **Automatic Agenda Slides**
Generate table of contents automatically.

```python
from content_enhancer import create_agenda_slide

sections = [
    'Introduction',
    'Main Topics',
    'Case Studies',
    'Conclusions'
]

create_agenda_slide(prs, sections, theme=theme)
```

---

## 📋 Complete Command Reference

### Basic Commands
```bash
# Convert single file
python main.py document.pdf

# Specify output name
python main.py notes.txt presentation.pptx

# Use custom theme
python main.py doc.pdf --theme modern

# Choose LLM provider
python main.py doc.pdf --provider openai

# Export to PDF
python main.py doc.pdf --export pdf

# Quiet mode (no banner)
python main.py doc.pdf --quiet
```

### Batch Processing
```bash
# Process multiple files
python main.py file1.txt file2.pdf --batch

# With wildcards
python main.py docs/*.md --batch

# Batch with export
python main.py *.pdf --batch --export html --theme vibrant
```

### Information Commands
```bash
# Show supported file formats
python main.py --formats

# Show available themes
python main.py --themes

# Show LLM providers
python main.py --providers

# Interactive mode
python main.py --interactive

# Show version
python main.py --version

# Show help
python main.py --help
```

---

## 🔧 Configuration

### Environment Variables
Set these in your environment or `.env` file:

```bash
# LLM API Keys
DEEPSEEK_API_KEY=your_deepseek_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Config.py Settings
Edit `config.py` to customize:

```python
# Default LLM provider
DEFAULT_LLM_PROVIDER = "deepseek"

# File processing limits
MAX_FILE_SIZE_MB = 50
MAX_INPUT_CHARS = 50000

# Image settings
MAX_IMAGES_PER_FILE = 20
MIN_IMAGE_SIZE = 100

# Batch settings
MAX_BATCH_FILES = 50
```

---

## 🎨 Available Themes

| Theme | Description | Best For |
|-------|-------------|----------|
| **Professional** | Clean & Business | Corporate presentations |
| **Modern** | Sleek & Contemporary | Tech/startup pitches |
| **Creative** | Bold & Expressive | Creative projects |
| **Corporate** | Formal & Traditional | Enterprise/finance |
| **Minimal** | Simple & Elegant | Academic/research |
| **Vibrant** | Colorful & Energetic | Marketing/sales |

---

## 💡 Tips & Best Practices

### For Best Results
1. **Provider Selection**:
   - DeepSeek: Best value, fast processing
   - OpenAI: Highest quality, detailed content
   - Claude: Best for complex documents
   - Ollama: Private/offline processing

2. **Batch Processing**:
   - Group similar documents
   - Use consistent naming
   - Monitor first few files for quality

3. **Export Options**:
   - PDF: For distribution/printing
   - HTML: For web sharing/interactive

4. **Image Handling**:
   - Works best with clear, high-res images
   - Automatically filters tiny icons
   - Images maintain aspect ratio

### Performance Tips
- Smaller files process faster
- Use `--quiet` for scripting
- Batch mode is more efficient than multiple commands
- Local Ollama is fastest for bulk processing

---

## 🐛 Troubleshooting

### Common Issues

**"Provider failed" error:**
- Check API key environment variable
- Verify account has credits/quota
- Try different provider with `--provider`

**PDF export fails:**
- Install LibreOffice: https://www.libreoffice.org/
- Or use `--export html` instead

**Images not showing:**
- Only works with PDF and DOCX
- Check source document has embedded images
- Min image size: 100x100 pixels

**Anthropic errors:**
- Install: `pip install anthropic`
- Set `ANTHROPIC_API_KEY` environment variable

---

## 📚 Examples

### Example 1: Research Paper to Presentation
```bash
# High-quality academic presentation
python main.py research_paper.pdf \
  --theme minimal \
  --provider openai \
  --export pdf
```

### Example 2: Multiple Reports
```bash
# Batch process quarterly reports
python main.py Q1_report.docx Q2_report.docx Q3_report.docx \
  --batch \
  --theme corporate \
  --export html
```

### Example 3: Quick Local Processing
```bash
# Fast local processing without API
python main.py notes.md \
  --provider ollama \
  --theme modern
```

### Example 4: Complete Workflow
```bash
# Full-featured conversion
python main.py whitepaper.pdf \
  --theme vibrant \
  --provider anthropic \
  --export pdf \
  presentation.pptx
```

---

## 🔐 Security Notes

### API Key Management
- Never commit API keys to version control
- Use environment variables
- Consider using `.env` file:
  ```bash
  # .env file
  DEEPSEEK_API_KEY=sk-xxx
  OPENAI_API_KEY=sk-xxx
  ANTHROPIC_API_KEY=sk-ant-xxx
  ```

### Data Privacy
- DeepSeek/OpenAI/Anthropic: Data sent to cloud
- Ollama: 100% local, no data leaves machine
- For sensitive documents: Use Ollama provider

---

## 📦 Installation

### Standard Install
```bash
pip install -r requirements.txt
```

### With Optional Dependencies
```bash
# For Anthropic Claude support
pip install anthropic

# For image handling
pip install pillow

# For local LLM support
pip install requests
```

### Full Install
```bash
pip install pillow requests anthropic pygments
```

---

## 🚀 What's Next?

Planned features for v4.0:
- AI-generated diagrams from text
- Custom PPTX templates
- Real-time collaboration
- Web interface
- Video export
- Animation effects

---

## 📞 Support

- Issues: Create GitHub issue
- Documentation: See README.md
- Examples: Check examples/ directory

**Version**: 3.0.0  
**Last Updated**: January 2026
