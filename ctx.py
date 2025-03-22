
✨ Analysis Complete
📂 Total files processed: 195
📜 Total lines of code: 195

[3m           📊 Code Statistics           [0m
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃[1;35m [0m[1;35mFile Type           [0m[1;35m [0m┃[1;35m [0m[1;35mFiles[0m[1;35m [0m┃[1;35m [0m[1;35mLines[0m[1;35m [0m┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━┩
│[36m [0m[36m../main.py          [0m[36m [0m│    15 │    15 │
│[36m [0m[36m../src/dir_walker.py[0m[36m [0m│    61 │    61 │
│[36m [0m[36m../src/choice.py    [0m[36m [0m│    43 │    43 │
│[36m [0m[36m../src/__init__.py  [0m[36m [0m│     0 │     0 │
│[36m [0m[36m../src/copy.py      [0m[36m [0m│     7 │     7 │
│[36m [0m[36m../src/arg_parser.py[0m[36m [0m│     9 │     9 │
│[36m [0m[36m../src/report.py    [0m[36m [0m│    60 │    60 │
└──────────────────────┴───────┴───────┘

🚀 Ready for LLM processing!
----- The start of file: ./main.py -----
from src.choice import make_language_choice
from src.dir_walker import dir_walker
from src.report import report, write_context, check_if_output_file_exist
from src.copy import copy_report

def main():
    ext = make_language_choice()
    output_file_name = 'ctx.' + ext
    check_if_output_file_exist(output_file_name)
    result = dir_walker(ext, output_file_name)
    report_text = report(result.summary, result.total_lines)
    write_context(report_text, output_file_name, result.file_contents)
    copy_report(report_text)
if __name__ == '__main__':
    main()

----- The end of file: ./main.py (строк: 15) -----

----- The start of file: ./src/dir_walker.py -----
import os
from typing import Dict, NamedTuple
from rich.progress import (  # Local import for thread safety
        Progress, 
        SpinnerColumn,
        TimeElapsedColumn,
        TextColumn,
    )

Summary = Dict[str, int]

class DirWalkerOutput(NamedTuple):
    summary: Summary
    total_lines: int
    file_contents: list[str]


def dir_walker(ext: str, output_file_name: str, additional_exclude_dirs: set[str] = set()) -> DirWalkerOutput:
    """Scan directories with progress visualization."""
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        transient=True,
    )
    
    progress.start()
    scan_task = progress.add_task(f"🔍 Scanning for {ext} files...", total=0)
    summary: Summary = {}
    total_lines = 0
    file_contents: list[str] = []
    exclude_dirs = {"vendor", ".idea", "node_modules", ".venv", "venv"}
    if additional_exclude_dirs is not set():
        exclude_dirs = exclude_dirs.union(additional_exclude_dirs)

    with progress:
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if not (file.endswith(ext) and file != output_file_name):
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        lines = f.readlines()
                    total_lines += len(lines)
                    summary[file_path] = len(lines)
                    progress.update(scan_task, advance=1)
                    file_contents.extend([
                        f"\n----- The start of file: {file_path} -----\n",
                        "".join(lines),
                        f"\n----- The end of file: {file_path} (строк: {len(lines)}) -----\n"
                    ])
                except (UnicodeDecodeError, PermissionError):
                    # Skip files we can't process, but continue processing others
                    continue
    return DirWalkerOutput(
        summary=summary,
        total_lines=total_lines,
        file_contents=file_contents
    )

----- The end of file: ./src/dir_walker.py (строк: 61) -----

----- The start of file: ./src/choice.py -----
from rich.prompt import Prompt
import os
from pathlib import Path
import platformdirs
import json

def make_language_choice() -> str:
    """Interactive language selection with persistence."""
    config_path = Path(platformdirs.user_config_dir("llm-code-ctx")) / "config.json"
    
    # Try to load saved preferences
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                prefs = json.load(f)
                if "language" in prefs:
                    if Prompt.ask(
                        f"⚙️  Use saved language preference [cyan]({prefs['language']})[/]?", 
                        choices=["y", "n"], 
                        default="y"
                    ) == "y":
                        return prefs['language']
        except Exception as e:
            print(f"The {e} is occured")
            pass
            
    # Interactive selection
    lang = Prompt.ask(
        "🔠 Choose language to analyze",
        choices=["py", "js", "ts", "java", "go"],
        default="py"
    )
    
    # Save preference
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump({"language": lang}, f)
    except Exception as e:
        print(f"The {e} is occured")
        pass
        
    return '.' + lang

----- The end of file: ./src/choice.py (строк: 43) -----

----- The start of file: ./src/__init__.py -----

----- The end of file: ./src/__init__.py (строк: 0) -----

----- The start of file: ./src/copy.py -----
import pyperclip

def copy_report(report: str) -> None:
    try:
        pyperclip.copy(report)
    except Exception as e:
        print(f"Error {e}\n While coping occured!")

----- The end of file: ./src/copy.py (строк: 7) -----

----- The start of file: ./src/arg_parser.py -----
import argparse
from .copy import copy_report

def parse_arg():
    parser = argparse.ArgumentParser(
        description="Purpose of the util is making UX with LLM and develoopment are better.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-copy", "--copy", )

----- The end of file: ./src/arg_parser.py (строк: 9) -----

----- The start of file: ./src/report.py -----
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

----- The end of file: ./src/report.py (строк: 60) -----
