from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class Product:
    name: str
    price: float
    expiry_date: date
    quantity: float  # в кг или шт


@dataclass
class Seller:
    name: str
    stall_number: int


@dataclass
class Buyer:
    name: str
    balance: float
    cart: List[Product]


@dataclass
class Promotion:
    name: str
    discount_percent: float
    applicable_products: List[str]


class Market:
    def __init__(self, name: str):
        self.name = name
        self.sellers: List[Seller] = []
        self.products: List[Product] = []
        self.promotions: List[Promotion] = []
        self.active_promotion: Optional[Promotion] = None

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def add_seller(self, seller: Seller) -> None:
        self.sellers.append(seller)

    def add_promotion(self, promotion: Promotion) -> None:
        self.promotions.append(promotion)