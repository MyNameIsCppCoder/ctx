from src.choice import make_language_choice
from src.dir_walker import dir_walker
from src.report import report, write_context, check_if_output_file_exist

def main():
    ext = make_language_choice()
    output_file_name = 'ctx' + ext
    check_if_output_file_exist(output_file_name)
    summary, total_lines = dir_walker(ext, output_file_name)
    report_text = report(summary, total_lines)
    write_context(report_text, output_file_name)

if __name__ == '__main__':
    main()
