import os
from .dir_walker import Summary

def estimate_tokens(report_text: str) -> int:
    return len(report_text.split()) // 4 if len(report_text.split()) != 0 else 0 

def report(summary: Summary, total_lines: int) -> str:
    report_text = '\n===== Report =====\n'
    for file_name, count in summary.items():
        report_text += f"File: {file_name}, count of lines: {count}\n"
    report_text += f"Total count of lines: {total_lines}\n"
    print(report_text)
    tokens = estimate_tokens(report_text)
    print(f"Примерное количество токенов: {tokens}")
    return report_text

def write_context(report_text: str, output_file_name: str, file_contents: list[str]) -> None:
    """Write both report and file contents to the output file"""
    with open(output_file_name, 'w', encoding='utf-8') as f:
        f.write(report_text)
        f.writelines(file_contents)

def check_if_output_file_exist(output_file_name: str) -> None:
    if os.path.exists(output_file_name):
        os.remove(output_file_name)
    return
