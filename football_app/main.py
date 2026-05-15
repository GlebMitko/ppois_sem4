import tkinter as tk
from model import FootballModel
from view import MainView
from controller import FootballController

if __name__ == "__main__":
    # Создаем главное окно
    root = tk.Tk()
    root.title("Футбольная команда - Управление игроками")
    root.geometry("1000x650")

    # Создаем модель и контроллер
    model = FootballModel()
    controller = FootballController(model, None)

    # Создаем представление (встраиваем в root)
    view = MainView(controller)
    controller.view = view
    view.pack(fill=tk.BOTH, expand=True)

    # Загружаем данные
    view.update_table(model.players)

    # Создаем меню (оно должно быть в root, а не в view)
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Меню "Файл"
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Файл", menu=file_menu)
    file_menu.add_command(label="Загрузить", command=controller.load_from_file)
    file_menu.add_command(label="Сохранить", command=controller.save_to_file)
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=root.quit)

    # Меню "Записи"
    record_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Записи", menu=record_menu)
    record_menu.add_command(label="Добавить", command=controller.add_record)
    record_menu.add_command(label="Поиск", command=controller.search_records)
    record_menu.add_command(label="Удалить по условию", command=controller.delete_records)

    # Запускаем приложение
    root.mainloop()