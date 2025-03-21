import os
from typing import Dict, NamedTuple

Summary = Dict[str, int]

class DirWalkerOutput(NamedTuple):
    summary: Summary
    total_lines: int


def dir_walker(ext: str, output_file_name: str, additional_exclude_dirs: set[str] = set()) -> DirWalkerOutput:
    summary: Summary = {}
    total_lines = 0
    exclude_dirs = {"vendor", ".idea", "node_modules", ".venv", "venv"}
    if additional_exclude_dirs is not set():
        exclude_dirs = exclude_dirs.union(additional_exclude_dirs)

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(ext) and file != output_file_name:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    summary[file_path] = len(lines)
                    with open(output_file_name, 'w', encoding='utf-8') as fo:
                        fo.write(f"\n----- The start of file: {file_path} -----\n")
                        for line in lines:
                            fo.write(line)
                        fo.write(f"----- The end of file: {file_path} (строк: {len(lines)}) -----\n")
    return DirWalkerOutput(summary=summary, total_lines=total_lines)
