import sys


def main():
    print("Выберите режим запуска:")
    print("1. CLI (консоль)")
    print("2. GUI (графический интерфейс)")

    choice = input("Ваш выбор: ")

    if choice == "1":
        from cli.cli_app import run_cli
        run_cli()
    elif choice == "2":
        from gui.gui_app import run_gui
        run_gui()
    else:
        print("Неверный выбор")
        sys.exit(1)


if __name__ == "__main__":
    main()