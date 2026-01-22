# Quick Reference Guide - AI PowerPoint Generator v3.0

## 🚀 Installation
```bash
pip install pillow requests
# Optional: pip install anthropic
```

## ⚡ Quick Commands

### Single File
```bash
python main.py document.pdf                    # Basic
python main.py doc.pdf output.pptx             # Custom name
python main.py doc.pdf -t modern               # With theme
python main.py doc.pdf -p openai               # With provider
python main.py doc.pdf -e pdf                  # Export to PDF
```

### Batch Processing
```bash
python main.py file1.txt file2.pdf -b          # Batch mode
python main.py *.md -b -t vibrant              # With theme
python main.py docs/*.pdf -b -p openai -e html # Full options
```

### Information
```bash
python main.py --help                          # Show help
python main.py --formats                       # Supported formats
python main.py --themes                        # Available themes
python main.py --providers                     # LLM providers
python main.py --interactive                   # Guided mode
```

## 🎨 Themes
- `professional` - Clean & Business (default)
- `modern` - Sleek & Contemporary
- `creative` - Bold & Expressive
- `corporate` - Formal & Traditional
- `minimal` - Simple & Elegant
- `vibrant` - Colorful & Energetic

## 🤖 Providers
- `deepseek` - Default, cost-effective
- `openai` - GPT-4, requires OPENAI_API_KEY
- `anthropic` - Claude, requires ANTHROPIC_API_KEY + pip install anthropic
- `ollama` - Local models, requires Ollama running

## 📤 Export Formats
- `pdf` - Requires LibreOffice or PowerPoint
- `html` - No dependencies, reveal.js slideshow

## 🔐 Environment Variables
```bash
# Set in your environment
export DEEPSEEK_API_KEY=sk-your-key-here
export OPENAI_API_KEY=sk-your-key-here
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## 📋 Supported Input Formats
TXT, MD, PDF, DOCX, CSV, JSON, XML, HTML, PY

## 🎯 Common Workflows

### Research Paper → PDF Presentation
```bash
python main.py paper.pdf -t minimal -p openai -e pdf
```

### Multiple Reports → HTML Presentations
```bash
python main.py Q*.docx -b -t corporate -e html
```

### Quick Local Conversion
```bash
python main.py notes.md -p ollama -t modern
```

### High-Quality Corporate Deck
```bash
python main.py whitepaper.pdf result.pptx -t corporate -p anthropic -e pdf
```

## 🐛 Troubleshooting

### "Provider failed"
- Check API key: `echo $OPENAI_API_KEY`
- Verify credits/quota on provider website
- Try different provider: `-p deepseek`

### "PDF export failed"
- Install LibreOffice: https://www.libreoffice.org/
- Or use HTML: `-e html`

### "Import error: anthropic"
- Install: `pip install anthropic`

### "No module named 'PIL'"
- Install: `pip install pillow`

## 💡 Pro Tips

1. **Best Provider Choice:**
   - Quick drafts: `deepseek`
   - High quality: `openai` or `anthropic`
   - Private docs: `ollama`
   - Cost-sensitive: `deepseek`

2. **Batch Processing:**
   - Group similar documents
   - Test first file before batch
   - Use `--quiet` for scripting

3. **Export Strategy:**
   - PDF for distribution
   - HTML for web sharing
   - PPTX for editing

4. **Performance:**
   - Smaller files process faster
   - Local Ollama fastest for bulk
   - Batch mode more efficient than loops

## 📁 File Structure
```
p10/
├── main.py                 # Entry point
├── config.py               # Configuration
├── llm_client.py           # LLM interface
├── llm_providers.py        # Provider implementations
├── pptx_generator.py       # PPTX creation
├── file_reader.py          # File reading
├── image_extractor.py      # Image extraction
├── chart_generator.py      # Chart creation
├── export_utils.py         # Format export
├── content_enhancer.py     # Advanced features
├── README.md               # Main docs
├── NEW_FEATURES.md         # Feature guide
└── IMPLEMENTATION_SUMMARY.md # Technical details
```

## 📞 Need Help?

1. Read [NEW_FEATURES.md](NEW_FEATURES.md) for detailed docs
2. Check [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details
3. Run `python main.py --help` for command reference
4. Try `python main.py --interactive` for guided mode

---

**Version:** 3.0.0 | **Updated:** January 2026
