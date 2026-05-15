from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QPushButton, QLineEdit, QMessageBox,
    QTabWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt


class MarketView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Продуктовый рынок")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        tabs = QTabWidget()

        # Вкладка "Товары"
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)
        self.products_table.setHorizontalHeaderLabels(["Название", "Цена", "Годен до", "Статус"])
        tabs.addTab(self.products_table, "Товары")

        # Вкладка "Корзина"
        self.cart_list = QListWidget()
        self.total_label = QLabel("Итого: 0 руб.")
        buy_btn = QPushButton("Оплатить")
        buy_btn.clicked.connect(self.buy_clicked)
        cart_layout = QVBoxLayout()
        cart_layout.addWidget(self.cart_list)
        cart_layout.addWidget(self.total_label)
        cart_layout.addWidget(buy_btn)
        cart_widget = QWidget()
        cart_widget.setLayout(cart_layout)
        tabs.addTab(cart_widget, "Корзина")

        # Вкладка "Действия"
        action_widget = QWidget()
        action_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название товара")
        add_btn = QPushButton("Добавить в корзину")
        add_btn.clicked.connect(self.add_clicked)
        bargain_btn = QPushButton("Торговаться")
        bargain_btn.clicked.connect(self.bargain_clicked)
        promo_btn = QPushButton("Активировать акцию")
        promo_btn.clicked.connect(self.promo_clicked)

        action_layout.addWidget(QLabel("Выберите товар:"))
        action_layout.addWidget(self.name_input)
        action_layout.addWidget(add_btn)
        action_layout.addWidget(bargain_btn)
        action_layout.addWidget(promo_btn)
        action_widget.setLayout(action_layout)
        tabs.addTab(action_widget, "Действия")

        layout.addWidget(tabs)
        self.setLayout(layout)

        # Сигналы (будет подключать Controller)
        self.buy_signal = None
        self.add_signal = None
        self.bargain_signal = None
        self.promo_signal = None

    def buy_clicked(self):
        if self.buy_signal:
            self.buy_signal()

    def add_clicked(self):
        if self.add_signal:
            self.add_signal(self.name_input.text())

    def bargain_clicked(self):
        if self.bargain_signal:
            self.bargain_signal(self.name_input.text())

    def promo_clicked(self):
        if self.promo_signal:
            self.promo_signal()

    def update_products(self, products):
        self.products_table.setRowCount(len(products))
        for row, p in enumerate(products):
            self.products_table.setItem(row, 0, QTableWidgetItem(p.name))
            self.products_table.setItem(row, 1, QTableWidgetItem(str(p.price)))
            self.products_table.setItem(row, 2, QTableWidgetItem(p.expiry_date.isoformat()))
            status = "Просрочен" if p.expiry_date < __import__('datetime').date.today() else "Годен"
            self.products_table.setItem(row, 3, QTableWidgetItem(status))

    def update_cart(self, cart, total):
        self.cart_list.clear()
        for p in cart:
            self.cart_list.addItem(f"{p.name} - {p.price} руб.")
        self.total_label.setText(f"Итого: {total} руб.")

    def show_message(self, title, text):
        QMessageBox.information(self, title, text)

    def show_error(self, title, text):
        QMessageBox.critical(self, title, text)