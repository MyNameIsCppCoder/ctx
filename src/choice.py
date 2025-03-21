def make_language_choice() -> str:
    print("Please, choice a language to parse: \n")
    print("1) .py \n")
    print("2) .go \n")
    print("3) .js \n")  # Исправлена опечатка с "1)" на "3)"
    print("If you hasn't seen expected language - input it like \".cs\"\n")
    lang_input = input("Language: ")
    try:
        choice = int(lang_input)  # Используем временную переменную
        if choice == 1:
            return '.py'
        elif choice == 2:
            return '.go'
        elif choice == 3:
            return '.js'
        else:
            print('Incorrect input! Please enter 1, 2, 3 or a language extension starting with "."')
            exit(0)
    except ValueError:
        if lang_input.startswith('.'):
            return lang_input
        else:
            print('Incorrect input! Please enter a number or a language extension starting with "."')
            exit(0)
