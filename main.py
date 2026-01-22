"""
PowerPoint Generator - Main Entry Point

A powerful CLI application that transforms documents into professional
PowerPoint presentations using AI (DeepSeek LLM).

Usage:
    python main.py <input_file> [output_file]
    python main.py --interactive
    python main.py --help

Examples:
    python main.py document.pdf
    python main.py notes.txt presentation.pptx
    python main.py data.csv output.pptx --theme modern
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box

from file_reader import read_file, get_file_info
from llm_client import generate_presentation_content
from pptx_generator import generate_pptx
from config import SUPPORTED_EXTENSIONS, THEMES, APP_NAME, APP_VERSION


console = Console()


def show_banner():
    """Display application banner."""
    banner = f"""
[bold cyan]╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   🎯 {APP_NAME}                                    ║
║   [dim]Transform any document into stunning presentations[/dim]    ║
║   [dim]Version {APP_VERSION}[/dim]                                            ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝[/bold cyan]
"""
    console.print(banner)


def show_supported_formats():
    """Display supported file formats in a table."""
    table = Table(
        title="📄 Supported File Formats",
        box=box.ROUNDED,
        header_style="bold magenta",
        show_lines=True
    )
    table.add_column("Extension", style="cyan", justify="center")
    table.add_column("Type", style="green")
    table.add_column("Description", style="white")
    
    descriptions = {
        '.txt': 'Plain text documents',
        '.md': 'Markdown documentation',
        '.py': 'Python source code',
        '.json': 'JSON data files',
        '.csv': 'Spreadsheet data',
        '.xml': 'XML markup files',
        '.html': 'Web pages',
        '.pdf': 'PDF documents',
        '.docx': 'Word documents',
    }
    
    for ext, file_type in SUPPORTED_EXTENSIONS.items():
        table.add_row(ext, file_type.title(), descriptions.get(ext, ''))
    
    console.print(table)


def show_themes():
    """Display available presentation themes."""
    table = Table(
        title="🎨 Available Themes",
        box=box.ROUNDED,
        header_style="bold magenta"
    )
    table.add_column("Theme", style="cyan", justify="center")
    table.add_column("Primary Color", style="green")
    table.add_column("Style", style="white")
    
    for name, theme in THEMES.items():
        table.add_row(name.title(), theme['primary_color'], theme['style'])
    
    console.print(table)


def get_output_path(input_file: str, output_file: Optional[str] = None) -> str:
    """Generate output file path based on input file name."""
    if output_file:
        if not output_file.endswith('.pptx'):
            output_file += '.pptx'
        return output_file
    
    input_path = Path(input_file)
    return str(input_path.with_suffix('.pptx'))


def interactive_mode():
    """Run in interactive mode with user prompts."""
    show_banner()
    console.print()
    
    # Show supported formats
    show_supported_formats()
    console.print()
    
    # Get input file
    while True:
        input_file = Prompt.ask(
            "[bold cyan]📁 Enter input file path[/bold cyan]",
            console=console
        )
        
        if not input_file:
            console.print("[yellow]⚠ Please enter a file path[/yellow]")
            continue
            
        input_path = Path(input_file)
        if not input_path.exists():
            console.print(f"[red]❌ File not found: {input_file}[/red]")
            continue
            
        ext = input_path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            console.print(f"[red]❌ Unsupported file type: {ext}[/red]")
            continue
        break
    
    # Get output file
    default_output = get_output_path(input_file)
    output_file = Prompt.ask(
        "[bold cyan]📤 Output file[/bold cyan]",
        default=default_output,
        console=console
    )
    
    # Show themes
    console.print()
    show_themes()
    console.print()
    
    # Select theme
    theme_choices = list(THEMES.keys())
    theme = Prompt.ask(
        "[bold cyan]🎨 Select theme[/bold cyan]",
        choices=theme_choices,
        default="professional",
        console=console
    )
    
    # Confirm
    console.print()
    console.print(Panel(
        f"[bold]Input:[/bold] {input_file}\n"
        f"[bold]Output:[/bold] {output_file}\n"
        f"[bold]Theme:[/bold] {theme.title()}",
        title="📋 Summary",
        border_style="cyan"
    ))
    
    if not Confirm.ask("\n[bold]Proceed with generation?[/bold]", default=True, console=console):
        console.print("[yellow]⚠ Operation cancelled[/yellow]")
        return
    
    console.print()
    run_generation(input_file, output_file, theme)


def run_generation(input_file: str, output_file: str, theme: str = "professional"):
    """Execute the presentation generation pipeline."""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
        transient=False
    ) as progress:
        
        # Create main task
        main_task = progress.add_task("[cyan]Generating presentation...", total=100)
        
        try:
            # Step 1: Read the input file (0-20%)
            progress.update(main_task, description="[cyan]📖 Reading input file...")
            file_info = get_file_info(input_file)
            file_content = read_file(input_file)
            progress.update(main_task, completed=20)
            
            console.print(f"   [dim]→ Read {len(file_content):,} characters from {file_info['type']} file[/dim]")
            
            # Step 2: Generate presentation content using LLM (20-80%)
            progress.update(main_task, description="[cyan]🤖 Analyzing content with AI...")
            file_name = Path(input_file).name
            
            # Show thinking animation
            presentation_data = generate_presentation_content(
                file_content, 
                file_name,
                progress_callback=lambda p: progress.update(main_task, completed=20 + int(p * 0.6))
            )
            
            slide_count = len(presentation_data.get('slides', []))
            progress.update(main_task, completed=80)
            console.print(f"   [dim]→ Generated {slide_count} slides with AI[/dim]")
            
            # Step 3: Create the PowerPoint file (80-100%)
            progress.update(main_task, description="[cyan]📊 Creating PowerPoint file...")
            output_path = get_output_path(input_file, output_file)
            generate_pptx(presentation_data, output_path, theme)
            progress.update(main_task, completed=100)
            
        except FileNotFoundError as e:
            progress.stop()
            console.print(f"\n[bold red]❌ Error:[/bold red] {e}")
            sys.exit(1)
        except ValueError as e:
            progress.stop()
            console.print(f"\n[bold red]❌ Error:[/bold red] {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            progress.stop()
            console.print("\n[yellow]⚠ Operation cancelled by user[/yellow]")
            sys.exit(0)
        except Exception as e:
            progress.stop()
            console.print(f"\n[bold red]❌ Unexpected error:[/bold red] {e}")
            raise
    
    # Success message
    console.print()
    console.print(Panel(
        f"[bold green]✨ Presentation created successfully![/bold green]\n\n"
        f"[bold]File:[/bold] {output_path}\n"
        f"[bold]Slides:[/bold] {slide_count}\n"
        f"[bold]Theme:[/bold] {theme.title()}",
        title="🎉 Complete",
        border_style="green"
    ))


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog='pptgen',
        description=f'{APP_NAME} - Transform documents into stunning presentations using AI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf                    # Basic usage
  %(prog)s notes.txt output.pptx           # Custom output name
  %(prog)s report.docx --theme modern      # With theme
  %(prog)s --interactive                   # Interactive mode
  %(prog)s --formats                       # Show supported formats
  %(prog)s --themes                        # Show available themes
"""
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Input file to convert (PDF, DOCX, TXT, MD, etc.)'
    )
    
    parser.add_argument(
        'output_file',
        nargs='?',
        help='Output PPTX file (default: input filename with .pptx extension)'
    )
    
    parser.add_argument(
        '-t', '--theme',
        choices=list(THEMES.keys()),
        default='professional',
        help='Presentation theme (default: professional)'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode with prompts'
    )
    
    parser.add_argument(
        '--formats',
        action='store_true',
        help='Show supported file formats'
    )
    
    parser.add_argument(
        '--themes',
        action='store_true',
        help='Show available presentation themes'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {APP_VERSION}'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Minimal output (no banner/progress)'
    )
    
    return parser


def main():
    """Main function to orchestrate the presentation generation."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle info flags
    if args.formats:
        show_supported_formats()
        return
    
    if args.themes:
        show_themes()
        return
    
    # Interactive mode
    if args.interactive:
        interactive_mode()
        return
    
    # Check for required input file
    if not args.input_file:
        show_banner()
        console.print()
        parser.print_help()
        console.print()
        console.print("[yellow]💡 Tip: Use --interactive for guided mode[/yellow]")
        sys.exit(0)
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        console.print(f"[bold red]❌ Error:[/bold red] File not found: {args.input_file}")
        sys.exit(1)
    
    ext = input_path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        console.print(f"[bold red]❌ Error:[/bold red] Unsupported file type: {ext}")
        console.print("[dim]Use --formats to see supported file types[/dim]")
        sys.exit(1)
    
    # Show banner (unless quiet mode)
    if not args.quiet:
        show_banner()
        console.print()
    
    # Run generation
    output_file = args.output_file or get_output_path(args.input_file)
    run_generation(args.input_file, output_file, args.theme)


if __name__ == "__main__":
    main()
