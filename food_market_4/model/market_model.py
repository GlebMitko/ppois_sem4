from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class Product:
    name: str
    price: float
    expiry_date: date
    quantity: float


@dataclass
class Seller:
    name: str
    stall_number: int


@dataclass
class Buyer:
    name: str
    balance: float


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