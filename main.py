"""
PowerPoint Generator - Main Entry Point

This application reads content from various file types and generates
a professional PowerPoint presentation using AI (DeepSeek LLM).

Usage:
    python main.py <input_file> [output_file]
    
Examples:
    python main.py document.pdf
    python main.py notes.txt presentation.pptx
    python main.py data.csv output.pptx
"""

import sys
from pathlib import Path

from file_reader import read_file
from llm_client import generate_presentation_content
from pptx_generator import generate_pptx


def get_output_path(input_file: str, output_file: str = None) -> str:
    """Generate output file path based on input file name."""
    if output_file:
        return output_file
    
    input_path = Path(input_file)
    return str(input_path.with_suffix('.pptx'))


def main():
    """Main function to orchestrate the presentation generation."""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nError: Please provide an input file path.")
        print("\nSupported file types: .txt, .md, .py, .json, .csv, .xml, .html, .pdf, .docx")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Step 1: Read the input file
        print(f"📖 Reading file: {input_file}")
        file_content = read_file(input_file)
        print(f"   ✓ Successfully read {len(file_content)} characters")
        
        # Step 2: Generate presentation content using LLM
        print(f"🤖 Analyzing content with AI...")
        file_name = Path(input_file).name
        presentation_data = generate_presentation_content(file_content, file_name)
        slide_count = len(presentation_data.get('slides', []))
        print(f"   ✓ Generated {slide_count} slides")
        
        # Step 3: Create the PowerPoint file
        output_path = get_output_path(input_file, output_file)
        print(f"📊 Creating PowerPoint: {output_path}")
        generate_pptx(presentation_data, output_path)
        print(f"   ✓ Presentation saved successfully!")
        
        print(f"\n✨ Done! Your presentation is ready: {output_path}")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
