import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from model import FootballPlayer


class AddPlayerDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Добавить игрока")
        self.geometry("500x500")
        self.resizable(False, False)

        # Делаем окно модальным
        self.transient(parent)
        self.grab_set()

        # Центрируем окно
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

        # Основной фрейм с отступом
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        tk.Label(main_frame, text="Добавление нового игрока",
                 font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Поля ввода
        fields = [
            ("ФИО:", "full_name"),
            ("Дата рождения (ГГГГ-ММ-ДД):", "birth_date"),
            ("Футбольная команда:", "team"),
            ("Домашний город:", "home_city"),
            ("Состав:", "lineup"),
            ("Позиция:", "position")
        ]

        self.entries = {}
        for i, (label, key) in enumerate(fields, start=1):
            # Метка
            tk.Label(main_frame, text=label, font=('Helvetica', 10), anchor='e').grid(
                row=i, column=0, padx=5, pady=8, sticky='e')
            # Поле ввода
            entry = tk.Entry(main_frame, width=30, font=('Helvetica', 10), relief=tk.SUNKEN, bd=1)
            entry.grid(row=i, column=1, padx=5, pady=8, sticky='w')
            self.entries[key] = entry

            # Подсказки для полей
            if key == "birth_date":
                entry.insert(0, "1990-01-01")
            elif key == "lineup":
                entry.insert(0, "Основной")
            elif key == "position":
                entry.insert(0, "Нападающий")

        # Кнопки
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="✅ Добавить", command=self.add_player,
                  bg='#4CAF50', fg='white', font=('Helvetica', 10, 'bold'),
                  padx=20, pady=5, relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="❌ Отмена", command=self.destroy,
                  bg='#f44336', fg='white', font=('Helvetica', 10, 'bold'),
                  padx=20, pady=5, relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=10)

        # Фокус на первое поле
        self.entries["full_name"].focus()

    def add_player(self):
        try:
            full_name = self.entries["full_name"].get().strip()
            if not full_name:
                messagebox.showerror("Ошибка", "ФИО обязательно для заполнения")
                return

            birth_date_str = self.entries["birth_date"].get().strip()
            if not birth_date_str:
                messagebox.showerror("Ошибка", "Дата рождения обязательна для заполнения")
                return

            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")

            player = FootballPlayer(
                full_name=full_name,
                birth_date=birth_date,
                team=self.entries["team"].get().strip() or "Не указана",
                home_city=self.entries["home_city"].get().strip() or "Не указан",
                lineup=self.entries["lineup"].get().strip() or "Запасной",
                position=self.entries["position"].get().strip() or "Не указана"
            )
            self.controller.model.add_player(player)
            self.controller.view.update_table(self.controller.model.players)
            messagebox.showinfo("Успех", f"Игрок '{full_name}' успешно добавлен!")
            self.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты!\nИспользуйте ГГГГ-ММ-ДД\nНапример: 1990-01-15")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


class SearchDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Поиск игроков")
        self.geometry("900x650")

        # Делаем окно модальным
        self.transient(parent)
        self.grab_set()

        # Центрируем окно
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

        # Основной контейнер
        main_frame = tk.Frame(self, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        tk.Label(main_frame, text="Поиск игроков по критериям",
                 font=('Helvetica', 14, 'bold')).pack(pady=(0, 15))

        # Рамка с условиями поиска
        criteria_frame = tk.LabelFrame(main_frame, text="Критерии поиска",
                                       font=('Helvetica', 10, 'bold'), padx=15, pady=10)
        criteria_frame.pack(fill=tk.X, pady=(0, 15))

        # Поля ввода (2 колонки)
        # Левая колонка
        left_frame = tk.Frame(criteria_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(left_frame, text="ФИО (часть):", font=('Helvetica', 10), anchor='e').grid(row=0, column=0, padx=5,
                                                                                           pady=8, sticky='e')
        self.full_name_entry = tk.Entry(left_frame, width=25, font=('Helvetica', 10), relief=tk.SUNKEN, bd=1)
        self.full_name_entry.grid(row=0, column=1, padx=5, pady=8, sticky='w')

        tk.Label(left_frame, text="Позиция:", font=('Helvetica', 10), anchor='e').grid(row=1, column=0, padx=5, pady=8,
                                                                                       sticky='e')
        self.position_entry = tk.Entry(left_frame, width=25, font=('Helvetica', 10), relief=tk.SUNKEN, bd=1)
        self.position_entry.grid(row=1, column=1, padx=5, pady=8, sticky='w')

        tk.Label(left_frame, text="Футбольная команда:", font=('Helvetica', 10), anchor='e').grid(row=2, column=0,
                                                                                                  padx=5, pady=8,
                                                                                                  sticky='e')
        self.team_entry = tk.Entry(left_frame, width=25, font=('Helvetica', 10), relief=tk.SUNKEN, bd=1)
        self.team_entry.grid(row=2, column=1, padx=5, pady=8, sticky='w')

        # Правая колонка
        right_frame = tk.Frame(criteria_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(right_frame, text="Дата рождения:", font=('Helvetica', 10), anchor='e').grid(row=0, column=0, padx=5,
                                                                                              pady=8, sticky='e')
        self.birth_date_entry = tk.Entry(right_frame, width=20, font=('Helvetica', 10), relief=tk.SUNKEN, bd=1)
        self.birth_date_entry.grid(row=0, column=1, padx=5, pady=8, sticky='w')
        tk.Label(right_frame, text="(ГГГГ-ММ-ДД)", font=('Helvetica', 8)).grid(row=0, column=2, padx=2)

        tk.Label(right_frame, text="Состав:", font=('Helvetica', 10), anchor='e').grid(row=1, column=0, padx=5, pady=8,
                                                                                       sticky='e')
        self.lineup_entry = tk.Entry(right_frame, width=20, font=('Helvetica', 10), relief=tk.SUNKEN, bd=1)
        self.lineup_entry.grid(row=1, column=1, padx=5, pady=8, sticky='w')

        tk.Label(right_frame, text="Домашний город:", font=('Helvetica', 10), anchor='e').grid(row=2, column=0, padx=5,
                                                                                               pady=8, sticky='e')
        self.city_entry = tk.Entry(right_frame, width=20, font=('Helvetica', 10), relief=tk.SUNKEN, bd=1)
        self.city_entry.grid(row=2, column=1, padx=5, pady=8, sticky='w')

        # Кнопка поиска
        btn_frame = tk.Frame(criteria_frame)
        btn_frame.pack(side=tk.BOTTOM, pady=10)

        tk.Button(btn_frame, text="🔍 Найти", command=self.search,
                  bg='#2196F3', fg='white', font=('Helvetica', 10, 'bold'),
                  padx=30, pady=5, relief=tk.RAISED, bd=2).pack()

        # Результаты поиска
        result_frame = tk.LabelFrame(main_frame, text="Результаты поиска",
                                     font=('Helvetica', 10, 'bold'), padx=10, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # Таблица результатов
        columns = ("ФИО", "Дата рождения", "Команда", "Город", "Состав", "Позиция")

        # Фрейм для таблицы и скроллбара
        tree_frame = tk.Frame(result_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.result_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.result_tree.heading(col, text=col)
            if col == "ФИО":
                self.result_tree.column(col, width=200)
            elif col == "Дата рождения":
                self.result_tree.column(col, width=100)
            else:
                self.result_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)

        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Счетчик результатов
        self.result_count_label = tk.Label(main_frame, text="Найдено записей: 0",
                                           font=('Helvetica', 9, 'italic'), fg='blue')
        self.result_count_label.pack(pady=(10, 0))

    def search(self):
        try:
            birth_date = None
            birth_date_str = self.birth_date_entry.get().strip()
            if birth_date_str:
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")

            players = self.controller.model.search_by_criteria(
                full_name=self.full_name_entry.get().strip(),
                birth_date=birth_date,
                position=self.position_entry.get().strip(),
                lineup=self.lineup_entry.get().strip(),
                team=self.team_entry.get().strip(),
                home_city=self.city_entry.get().strip()
            )

            # Очищаем таблицу
            for row in self.result_tree.get_children():
                self.result_tree.delete(row)

            # Заполняем результаты
            for p in players:
                self.result_tree.insert("", tk.END, values=(
                    p.full_name,
                    p.birth_date.strftime("%d.%m.%Y"),
                    p.team,
                    p.home_city,
                    p.lineup,
                    p.position
                ))

            # Обновляем счетчик
            count = len(players)
            self.result_count_label.config(text=f"Найдено записей: {count}")

            if count == 0:
                messagebox.showinfo("Поиск", "По вашему запросу ничего не найдено")
            else:
                messagebox.showinfo("Поиск", f"Найдено записей: {count}")

        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты!\nИспользуйте ГГГГ-ММ-ДД")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при поиске: {e}")


class DeleteDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Удаление записей")
        self.geometry("600x600")
        self.resizable(False, False)

        # Делаем окно модальным
        self.transient(parent)
        self.grab_set()

        # Центрируем окно
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 400) // 2
        self.geometry(f"+{x}+{y}")

        # Поля для условий
        self.entries = {}

        # ФИО
        tk.Label(self, text="ФИО (часть):").pack(padx=10, pady=5)
        self.entries['full_name'] = tk.Entry(self, width=40)
        self.entries['full_name'].pack(padx=10, pady=5)

        # Дата рождения
        tk.Label(self, text="Дата рождения (ГГГГ-ММ-ДД):").pack(padx=10, pady=5)
        self.entries['birth_date'] = tk.Entry(self, width=40)
        self.entries['birth_date'].pack(padx=10, pady=5)

        # Позиция
        tk.Label(self, text="Позиция:").pack(padx=10, pady=5)
        self.entries['position'] = tk.Entry(self, width=40)
        self.entries['position'].pack(padx=10, pady=5)

        # Состав
        tk.Label(self, text="Состав:").pack(padx=10, pady=5)
        self.entries['lineup'] = tk.Entry(self, width=40)
        self.entries['lineup'].pack(padx=10, pady=5)

        # Команда
        tk.Label(self, text="Футбольная команда:").pack(padx=10, pady=5)
        self.entries['team'] = tk.Entry(self, width=40)
        self.entries['team'].pack(padx=10, pady=5)

        # Город
        tk.Label(self, text="Домашний город:").pack(padx=10, pady=5)
        self.entries['home_city'] = tk.Entry(self, width=40)
        self.entries['home_city'].pack(padx=10, pady=5)

        # Предупреждение
        warning_label = tk.Label(self, text="⚠ ВНИМАНИЕ: Записи будут удалены навсегда!",
                                 fg='red', font=('Helvetica', 9, 'bold'))
        warning_label.pack(pady=10)

        # Кнопки
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        delete_btn = tk.Button(button_frame, text="Удалить", command=self.delete_players,
                               bg='red', fg='white', padx=20, pady=5, width=10)
        delete_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(button_frame, text="Отмена", command=self.destroy,
                               padx=20, pady=5, width=10)
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def delete_players(self):
        try:
            # Запрашиваем подтверждение
            if not messagebox.askyesno("Подтверждение удаления",
                                       "Вы уверены, что хотите удалить записи?\n\nЭто действие нельзя отменить!"):
                return

            # Получаем дату рождения
            birth_date = None
            birth_date_str = self.entries['birth_date'].get().strip()
            if birth_date_str:
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")

            # Выполняем удаление
            count = self.controller.model.delete_by_criteria(
                full_name=self.entries['full_name'].get().strip(),
                birth_date=birth_date,
                position=self.entries['position'].get().strip(),
                lineup=self.entries['lineup'].get().strip(),
                team=self.entries['team'].get().strip(),
                home_city=self.entries['home_city'].get().strip()
            )

            # Показываем результат
            if count > 0:
                messagebox.showinfo("Удаление", f"✅ Удалено записей: {count}")
                self.controller.view.update_table(self.controller.model.players)
                self.destroy()
            else:
                messagebox.showwarning("Удаление", "Записи по заданным условиям не найдены")

        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты!\nИспользуйте ГГГГ-ММ-ДД\nПример: 1990-01-15")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")