from tkinter import filedialog, messagebox
from dialogs import AddPlayerDialog, SearchDialog, DeleteDialog


class FootballController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def add_record(self):
        AddPlayerDialog(self.view, self)

    def search_records(self):
        SearchDialog(self.view, self)

    def delete_records(self):
        DeleteDialog(self.view, self)

    def save_to_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if filename:
            self.model.save_to_xml(filename)
            messagebox.showinfo("Сохранение", "Данные сохранены")

    def load_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filename:
            self.model.load_from_xml(filename)
            self.view.update_table(self.model.players)
            messagebox.showinfo("Загрузка", "Данные загружены")