from datetime import date
from typing import List, Tuple
from .market_model import Product, Buyer, Market, Promotion


class ProductExpiredError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


def select_products(
    buyer: Buyer,
    available_products: List[Product],
    chosen_names: List[str]
) -> Tuple[Buyer, List[Product], float]:
    chosen = []
    total = 0.0
    for name in chosen_names:
        for p in available_products:
            if p.name.lower() == name.lower():
                if p.expiry_date < date.today():
                    raise ProductExpiredError(f"Продукт {p.name} просрочен!")
                chosen.append(p)
                total += p.price
                break
        else:
            raise ProductNotFoundError(f"Продукт {name} не найден")
    return buyer, chosen, total


def bargain_price(original_price: float, offered_price: float) -> float:
    if offered_price <= 0:
        raise ValueError("Цена должна быть положительной")
    return round((original_price + offered_price) / 2, 2)


def calculate_total(cart: List[Product], market: Market) -> float:
    total = sum(p.price for p in cart)
    if market.active_promotion:
        applicable = [p for p in cart if p.name in market.active_promotion.applicable_products]
        if applicable:
            discount = sum(p.price for p in applicable) * market.active_promotion.discount_percent / 100
            total -= discount
    return round(total, 2)


def checkout(buyer: Buyer, cart: List[Product], market: Market) -> Tuple[Buyer, List[Product]]:
    total = calculate_total(cart, market)
    if buyer.balance < total:
        raise InsufficientFundsError(f"Не хватает {total - buyer.balance:.2f} руб.")
    buyer.balance -= total
    return buyer, []


def check_expired(products: List[Product]) -> List[Product]:
    today = date.today()
    return [p for p in products if p.expiry_date < today]