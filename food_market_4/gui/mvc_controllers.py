from PyQt5.QtWidgets import QApplication
from model.market_model import Market, Buyer, Product, Seller, Promotion
from model.market_service import (
    select_products, bargain_price, calculate_total, checkout, check_expired,
    ProductExpiredError, InsufficientFundsError, ProductNotFoundError
)
from datetime import date, timedelta


class MarketController:
    def __init__(self, view):
        self.view = view
        self.market = Market("Центральный рынок")
        self.buyer = Buyer("Алексей", 500.0)
        self.cart = []

        # Инициализация данных
        self.market.sellers.append(Seller("Иван", 1))
        self.market.products = [
            Product("Яблоки", 120.0, date.today() + timedelta(days=5), 2.0),
            Product("Молоко", 80.0, date.today() - timedelta(days=1), 1.0),
            Product("Хлеб", 50.0, date.today() + timedelta(days=2), 1.0)
        ]
        self.market.promotions.append(Promotion("Скидка на фрукты", 10.0, ["Яблоки"]))

        # Подключаем сигналы View
        self.view.buy_signal = self.checkout
        self.view.add_signal = self.add_to_cart
        self.view.bargain_signal = self.bargain
        self.view.promo_signal = self.activate_promo

        # Начальное обновление
        self.view.update_products(self.market.products)
        self.update_cart_view()

    def add_to_cart(self, product_name):
        try:
            _, new_products, _ = select_products(
                self.buyer, self.market.products, [product_name]
            )
            self.cart.extend(new_products)
            self.update_cart_view()
            self.view.show_message("Успех", f"{product_name} добавлен в корзину")
        except (ProductExpiredError, ProductNotFoundError) as e:
            self.view.show_error("Ошибка", str(e))

    def bargain(self, product_name):
        for p in self.market.products:
            if p.name.lower() == product_name.lower():
                try:
                    offered = float(input("Цена для торга: "))
                    final = bargain_price(p.price, offered)
                    self.view.show_message("Торг", f"Продавец согласен на {final} руб.")
                except ValueError:
                    self.view.show_error("Ошибка", "Некорректная цена")
                return
        self.view.show_error("Ошибка", "Товар не найден")

    def activate_promo(self):
        if self.market.promotions:
            self.market.active_promotion = self.market.promotions[0]
            self.view.show_message("Акция", f"Акция '{self.market.active_promotion.name}' активирована")
            self.update_cart_view()
        else:
            self.view.show_error("Ошибка", "Нет доступных акций")

    def update_cart_view(self):
        total = calculate_total(self.cart, self.market)
        self.view.update_cart(self.cart, total)

    def checkout(self):
        try:
            self.buyer, self.cart = checkout(self.buyer, self.cart, self.market)
            self.update_cart_view()
            self.view.show_message("Оплата", f"Оплачено. Баланс: {self.buyer.balance} руб.")
        except InsufficientFundsError as e:
            self.view.show_error("Ошибка", str(e))