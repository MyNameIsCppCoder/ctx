import os
from .dir_walker import Summary
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.theme import Theme


def estimate_tokens(report_text: str) -> int:
    return len(report_text.split()) // 4 if len(report_text.split()) != 0 else 0 

def report(summary: Summary, total_lines: int) -> str:
    """Generate formatted report with rich styling."""
    console = Console()
    
    # Create summary table
    table = Table(title="📊 Code Statistics", show_header=True, header_style="bold magenta")
    table.add_column("File Type", style="cyan")
    table.add_column("Files", justify="right")
    table.add_column("Lines", justify="right")
    
    for ext, count in summary.items():
        table.add_row(f".{ext}", str(count), str(summary.get(ext, 0)))
    
    # Prepare report text
    report_text = Text()
    report_text.append("\n✨ Analysis Complete\n", style="bold green")
    report_text.append(f"📂 Total files processed: {sum(summary.values())}\n")
    report_text.append(f"📜 Total lines of code: {total_lines}\n\n")
    
    # Render table to text
    with console.capture() as capture:
        console.print(table)
    report_text.append(capture.get())
    
    report_text.append("\n🚀 Ready for LLM processing!", style="bold blue")
    
    return report_text.plain

def write_context(report_text: str, output_file_name: str, file_contents: list[str]) -> None:
    """Write both report and file contents to the output file"""
    with open(output_file_name, 'w', encoding='utf-8') as f:
        f.write(report_text)
        f.writelines(file_contents)


console = Console(theme=Theme({"success": "bold green", "warning": "bold yellow", "error": "bold red"}))

def check_if_output_file_exist(output_file_name: str) -> None:
    """Check if output file exists with interactive confirmation."""
    if os.path.exists(output_file_name):
        if not Prompt.ask(
            f"[warning]⚠️  File {output_file_name} exists. Overwrite?[/]", 
            choices=["y", "n"], 
            default="n"
        ) == "y":
            console.print("[error]✖ Operation cancelled[/]")
            raise SystemExit(1)
        console.print(f"[success]✔ Will overwrite {output_file_name}[/]")
