from model.market_model import Market, Buyer, Product, Seller, Promotion
from model.market_service import (
    select_products, bargain_price, calculate_total, checkout, check_expired,
    ProductExpiredError, InsufficientFundsError, ProductNotFoundError
)
from datetime import date, timedelta


def run_cli():
    market = Market("Центральный рынок")
    market.sellers.append(Seller("Иван", 1))
    market.products = [
        Product("Яблоки", 120.0, date.today() + timedelta(days=5), 2.0),
        Product("Молоко", 80.0, date.today() - timedelta(days=1), 1.0),
        Product("Хлеб", 50.0, date.today() + timedelta(days=2), 1.0)
    ]
    market.promotions.append(Promotion("Скидка на фрукты", 10.0, ["Яблоки"]))

    buyer = Buyer("Алексей", 500.0)
    cart = []

    while True:
        print("\n===== ПРОДУКТОВЫЙ РЫНОК (CLI) =====")
        print("1. Товары")
        print("2. Выбрать товары")
        print("3. Торг")
        print("4. Акция")
        print("5. Корзина")
        print("6. Оплатить")
        print("7. Просрочка")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            for p in market.products:
                status = "просрочен" if p.expiry_date < date.today() else "годен"
                print(f"{p.name} - {p.price} руб. ({status})")

        elif choice == "2":
            names = input("Товары через запятую: ").split(",")
            try:
                buyer, new_cart, _ = select_products(buyer, market.products, [n.strip() for n in names])
                cart.extend(new_cart)
                print("Добавлено")
            except (ProductExpiredError, ProductNotFoundError) as e:
                print(f"Ошибка: {e}")

        elif choice == "3":
            name = input("Название товара: ")
            for p in market.products:
                if p.name.lower() == name.lower():
                    try:
                        offer = float(input("Ваша цена: "))
                        final = bargain_price(p.price, offer)
                        print(f"Цена после торга: {final} руб.")
                    except ValueError:
                        print("Неверная цена")
                    break
            else:
                print("Товар не найден")

        elif choice == "4":
            if market.promotions:
                market.active_promotion = market.promotions[0]
                print(f"Акция '{market.active_promotion.name}' активирована")

        elif choice == "5":
            if not cart:
                print("Корзина пуста")
            else:
                for p in cart:
                    print(f"{p.name} - {p.price} руб.")
                print(f"Итого: {calculate_total(cart, market)} руб.")

        elif choice == "6":
            try:
                buyer, cart = checkout(buyer, cart, market)
                print(f"Оплачено. Баланс: {buyer.balance} руб.")
            except InsufficientFundsError as e:
                print(f"Ошибка: {e}")

        elif choice == "7":
            expired = check_expired(market.products)
            for p in expired:
                print(f"Просрочен: {p.name}")

        elif choice == "0":
            break