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
                except (UnicodeDecodeError, PermissionError) as e:
                    # Skip files we can't process, but continue processing others
                    continue
                        f"\n----- The start of file: {file_path} -----\n",
                        "".join(lines),
                        f"\n----- The end of file: {file_path} (строк: {len(lines)}) -----\n"
                    ])
    return DirWalkerOutput(
        summary=summary,
        total_lines=total_lines,
        file_contents=file_contents
    )
