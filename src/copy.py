import pyperclip

def copy_report(report: str) -> None:
    try:
        pyperclip.copy(report)
    except Exception as e:
        print(f"Error {e}\n While coping occured!")
