from datetime import date
from typing import List
from models import Product, Buyer, Market, Promotion


class ProductExpiredError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


def select_products(buyer: Buyer, available_products: List[Product], chosen_names: List[str]) -> Buyer:
    chosen = []
    for name in chosen_names:
        for p in available_products:
            if p.name.lower() == name.lower():
                if p.expiry_date < date.today():
                    raise ProductExpiredError(f"Продукт {p.name} просрочен!")
                chosen.append(p)
                break
        else:
            raise ProductNotFoundError(f"Продукт {name} не найден")
    buyer.cart.extend(chosen)
    return buyer


def bargain_with_seller(buyer: Buyer, product: Product, offered_price: float) -> float:
    if offered_price <= 0:
        raise ValueError("Цена торга должна быть положительной")
    final_price = (product.price + offered_price) / 2
    return round(final_price, 2)


def calculate_total(buyer: Buyer, market: Market) -> float:
    total = sum(p.price for p in buyer.cart)
    if market.active_promotion:
        applicable = [p for p in buyer.cart if p.name in market.active_promotion.applicable_products]
        if applicable:
            discount = sum(p.price for p in applicable) * market.active_promotion.discount_percent / 100
            total -= discount
    return round(total, 2)


def checkout(buyer: Buyer, market: Market) -> Buyer:
    total = calculate_total(buyer, market)
    if buyer.balance < total:
        raise InsufficientFundsError(f"Не хватает {total - buyer.balance:.2f} руб.")
    buyer.balance -= total
    buyer.cart.clear()
    return buyer


def check_expiry(products: List[Product]) -> List[Product]:
    today = date.today()
    return [p for p in products if p.expiry_date < today]