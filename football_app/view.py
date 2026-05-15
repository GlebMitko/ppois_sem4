import tkinter as tk
from tkinter import ttk
from datetime import datetime
from dialogs import AddPlayerDialog, SearchDialog, DeleteDialog


class MainView(tk.Frame):  # Наследуемся от Frame, а не от Tk
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.current_page = 0
        self.rows_per_page = 10
        self.current_data = []

        # Создаем все элементы интерфейса
        self._create_toolbar()
        self._create_table()
        self._create_pagination()

        # Принудительное обновление
        self.update_idletasks()

    def _create_toolbar(self):
        # Верхняя панель с кнопками
        toolbar = tk.Frame(self, bg='lightgray', height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar.pack_propagate(False)

        # Кнопки на панели
        btn_frame = tk.Frame(toolbar, bg='lightgray')
        btn_frame.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(btn_frame, text="📁 Загрузить", command=self.controller.load_from_file,
                  bg='lightgray', relief=tk.RAISED, padx=10, pady=3).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="💾 Сохранить", command=self.controller.save_to_file,
                  bg='lightgray', relief=tk.RAISED, padx=10, pady=3).pack(side=tk.LEFT, padx=2)

        tk.Button(btn_frame, text="➕ Добавить", command=self.controller.add_record,
                  bg='lightgray', relief=tk.RAISED, padx=10, pady=3).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🔍 Поиск", command=self.controller.search_records,
                  bg='lightgray', relief=tk.RAISED, padx=10, pady=3).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🗑 Удалить", command=self.controller.delete_records,
                  bg='lightgray', relief=tk.RAISED, padx=10, pady=3).pack(side=tk.LEFT, padx=2)

    def _create_table(self):
        # Создаем фрейм для таблицы
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Стиль для таблицы
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 10))
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Колонки таблицы
        columns = ("ФИО", "Дата рождения", "Команда", "Город", "Состав", "Позиция")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        # Настройка колонок
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ФИО":
                self.tree.column(col, width=200)
            elif col == "Дата рождения":
                self.tree.column(col, width=100)
            elif col == "Команда":
                self.tree.column(col, width=120)
            elif col == "Город":
                self.tree.column(col, width=120)
            else:
                self.tree.column(col, width=100)

        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_pagination(self):
        # Нижняя панель с пагинацией
        pag_frame = tk.Frame(self, bg='lightgray', height=50)
        pag_frame.pack(side=tk.BOTTOM, fill=tk.X)
        pag_frame.pack_propagate(False)

        # Кнопки навигации
        nav_frame = tk.Frame(pag_frame, bg='lightgray')
        nav_frame.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(nav_frame, text="<<", command=self.first_page,
                  width=3, bg='lightgray', relief=tk.RAISED).pack(side=tk.LEFT, padx=2)
        tk.Button(nav_frame, text="<", command=self.prev_page,
                  width=3, bg='lightgray', relief=tk.RAISED).pack(side=tk.LEFT, padx=2)
        tk.Button(nav_frame, text=">", command=self.next_page,
                  width=3, bg='lightgray', relief=tk.RAISED).pack(side=tk.LEFT, padx=2)
        tk.Button(nav_frame, text=">>", command=self.last_page,
                  width=3, bg='lightgray', relief=tk.RAISED).pack(side=tk.LEFT, padx=2)

        # Настройка количества записей
        settings_frame = tk.Frame(pag_frame, bg='lightgray')
        settings_frame.pack(side=tk.LEFT, padx=20, pady=10)

        tk.Label(settings_frame, text="Записей на странице:", bg='lightgray').pack(side=tk.LEFT, padx=5)
        self.rows_per_page_var = tk.StringVar(value="10")
        rows_spin = tk.Spinbox(settings_frame, from_=5, to=50, textvariable=self.rows_per_page_var,
                               command=self.change_rows_per_page, width=5)
        rows_spin.pack(side=tk.LEFT, padx=2)

        # Информационная панель
        self.info_label = tk.Label(pag_frame, text="", bg='lightgray', font=('Helvetica', 10))
        self.info_label.pack(side=tk.RIGHT, padx=10, pady=10)

    def update_table(self, players):
        """Обновление таблицы данными"""
        self.current_data = players
        self.current_page = 0
        self._refresh_table()

    def _refresh_table(self):
        """Обновление отображения текущей страницы"""
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Рассчитываем текущую страницу
        start = self.current_page * self.rows_per_page
        end = start + self.rows_per_page
        page_players = self.current_data[start:end]

        # Заполняем таблицу
        for p in page_players:
            self.tree.insert("", tk.END, values=(
                p.full_name,
                p.birth_date.strftime("%d.%m.%Y"),
                p.team,
                p.home_city,
                p.lineup,
                p.position
            ))

        # Обновляем информационную панель
        total_pages = (len(self.current_data) + self.rows_per_page - 1) // self.rows_per_page
        if total_pages == 0:
            total_pages = 1

        self.info_label.config(
            text=f"Страница {self.current_page + 1} из {total_pages} | "
                 f"Всего записей: {len(self.current_data)} | "
                 f"На странице: {len(page_players)}"
        )

    def next_page(self):
        """Следующая страница"""
        total_pages = (len(self.current_data) + self.rows_per_page - 1) // self.rows_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self._refresh_table()

    def prev_page(self):
        """Предыдущая страница"""
        if self.current_page > 0:
            self.current_page -= 1
            self._refresh_table()

    def first_page(self):
        """Первая страница"""
        self.current_page = 0
        self._refresh_table()

    def last_page(self):
        """Последняя страница"""
        total_pages = (len(self.current_data) + self.rows_per_page - 1) // self.rows_per_page
        self.current_page = max(0, total_pages - 1)
        self._refresh_table()

    def change_rows_per_page(self):
        """Изменение количества записей на странице"""
        try:
            new_value = int(self.rows_per_page_var.get())
            if new_value > 0:
                self.rows_per_page = new_value
                self.current_page = 0
                self._refresh_table()
        except:
            pass