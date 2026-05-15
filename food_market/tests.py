import unittest
from datetime import date, timedelta
from models import Product, Buyer, Market, Promotion
from services import (
    select_products, calculate_total, checkout,
    check_expiry, ProductExpiredError, InsufficientFundsError, ProductNotFoundError
)


class TestMarketServices(unittest.TestCase):

    def setUp(self):
        self.market = Market("Тестовый рынок")
        self.fresh = Product("Сыр", 300.0, date.today() + timedelta(days=10), 0.5)
        self.expired = Product("Кефир", 70.0, date.today() - timedelta(days=1), 1.0)
        self.market.products = [self.fresh, self.expired]
        self.buyer = Buyer("Мария", 500.0, [])

    def test_select_products_success(self):
        buyer = select_products(self.buyer, self.market.products, ["Сыр"])
        self.assertEqual(len(buyer.cart), 1)
        self.assertEqual(buyer.cart[0].name, "Сыр")

    def test_select_products_expired(self):
        with self.assertRaises(ProductExpiredError):
            select_products(self.buyer, self.market.products, ["Кефир"])

    def test_select_products_not_found(self):
        with self.assertRaises(ProductNotFoundError):
            select_products(self.buyer, self.market.products, ["Ананас"])

    def test_calculate_total_with_promotion(self):
        self.buyer.cart = [self.fresh]
        promo = Promotion("Скидка на сыр", 20.0, ["Сыр"])
        self.market.active_promotion = promo
        total = calculate_total(self.buyer, self.market)
        self.assertEqual(total, 240.0)  # 300 - 20%

    def test_checkout_insufficient_funds(self):
        self.buyer.cart = [self.fresh]
        self.buyer.balance = 100.0
        with self.assertRaises(InsufficientFundsError):
            checkout(self.buyer, self.market)

    def test_checkout_success(self):
        self.buyer.cart = [self.fresh]
        self.buyer.balance = 500.0
        updated = checkout(self.buyer, self.market)
        self.assertEqual(updated.balance, 200.0)
        self.assertEqual(len(updated.cart), 0)

    def test_check_expiry(self):
        expired_list = check_expiry(self.market.products)
        self.assertEqual(len(expired_list), 1)
        self.assertEqual(expired_list[0].name, "Кефир")


if __name__ == "__main__":
    unittest.main()