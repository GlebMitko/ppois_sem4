from models import Market, Buyer, Product, Seller, Promotion
from services import (
    select_products, bargain_with_seller, checkout,
    check_expiry, ProductExpiredError, InsufficientFundsError, ProductNotFoundError
)
from datetime import date, timedelta


def display_menu():
    print("\n===== ПРОДУКТОВЫЙ РЫНОК =====")
    print("1. Посмотреть доступные товары")
    print("2. Выбрать товары в корзину")
    print("3. Поторговаться с продавцом")
    print("4. Применить акцию")
    print("5. Показать корзину и итоговую сумму")
    print("6. Оплатить покупку")
    print("7. Проверить просроченные товары")
    print("0. Выход")


def run_cli():
    market = Market("Центральный рынок")
    # Добавляем тестовых продавцов и товары
    seller1 = Seller("Иван", 1)
    market.add_seller(seller1)
    market.products.extend([
        Product("Яблоки", 120.0, date.today() + timedelta(days=5), 2.0),
        Product("Молоко", 80.0, date.today() - timedelta(days=1), 1.0),
        Product("Хлеб", 50.0, date.today() + timedelta(days=2), 1.0)
    ])
    market.promotions.append(Promotion("Скидка на фрукты", 10.0, ["Яблоки"]))

    buyer = Buyer("Алексей", 500.0, [])

    while True:
        display_menu()
        choice = input("Ваш выбор: ")

        if choice == "1":
            print("\nТовары на рынке:")
            for p in market.products:
                status = "просрочен" if p.expiry_date < date.today() else "годен"
                print(f"  {p.name} - {p.price} руб. ({status} до {p.expiry_date})")

        elif choice == "2":
            print("Введите названия товаров через запятую:")
            names = [n.strip() for n in input().split(",")]
            try:
                buyer = select_products(buyer, market.products, names)
                print("Товары добавлены в корзину.")
            except (ProductExpiredError, ProductNotFoundError) as e:
                print(f"Ошибка: {e}")

        elif choice == "3":
            print("С каким товаром торгуете?")
            prod_name = input("Название: ")
            for p in market.products:
                if p.name.lower() == prod_name.lower():
                    try:
                        price = float(input("Ваша цена: "))
                        final = bargain_with_seller(buyer, p, price)
                        print(f"Продавец согласился на {final} руб.")
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                    break
            else:
                print("Товар не найден")

        elif choice == "4":
            if market.promotions:
                market.active_promotion = market.promotions[0]
                print(f"Акция '{market.active_promotion.name}' активирована!")
            else:
                print("Нет активных акций")

        elif choice == "5":
            if not buyer.cart:
                print("Корзина пуста.")
            else:
                print("\nКорзина:")
                for p in buyer.cart:
                    print(f"  {p.name} - {p.price} руб.")
                from services import calculate_total
                print(f"Итого с учётом акций: {calculate_total(buyer, market)} руб.")

        elif choice == "6":
            try:
                buyer = checkout(buyer, market)
                print("Оплата прошла успешно! Корзина очищена.")
                print(f"Баланс покупателя: {buyer.balance:.2f} руб.")
            except InsufficientFundsError as e:
                print(f"Ошибка: {e}")

        elif choice == "7":
            expired = check_expiry(market.products)
            if expired:
                print("Просроченные товары:")
                for p in expired:
                    print(f"  {p.name} (годен до {p.expiry_date})")
            else:
                print("Все товары свежие.")

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный ввод, попробуйте снова.")