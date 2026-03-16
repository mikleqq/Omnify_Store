from __future__ import annotations
import uuid
from datetime import datetime

class Order:


    def __init__(self):
        self.order_id: str = str(uuid.uuid4())[:8].upper()
        self.created_at: str = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.items: list[dict] = []
        self.customer: dict = {}
        self.delivery_method: str = "courier"
        self.delivery_address: str = ""
        self.payment_method: str = "card"
        self.coupon_code: str = ""
        self.discount_pct: float = 0.0
        self.subtotal: float = 0.0
        self.delivery_cost: float = 0.0
        self.total: float = 0.0
        self.decorations: list[str] = []
        self.status: str = "pending"

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "created_at": self.created_at,
            "items": self.items,
            "customer": self.customer,
            "delivery_method": self.delivery_method,
            "delivery_address": self.delivery_address,
            "payment_method": self.payment_method,
            "coupon_code": self.coupon_code,
            "discount_pct": self.discount_pct,
            "subtotal": self.subtotal,
            "delivery_cost": self.delivery_cost,
            "total": self.total,
            "decorations": self.decorations,
            "status": self.status,
        }


class OrderBuilder:


    def __init__(self):
        self._order = Order()

    def set_items(self, items: list[dict]) -> OrderBuilder:
        self._order.items = items
        self._order.subtotal = sum(i["price"] * i["quantity"] for i in items)
        return self

    def set_customer(self, name: str, email: str, phone: str = "") -> OrderBuilder:
        self._order.customer = {"name": name, "email": email, "phone": phone}
        return self

    def set_delivery(self, method: str, address: str = "", cost: float = 0.0) -> OrderBuilder:
        self._order.delivery_method = method
        self._order.delivery_address = address
        self._order.delivery_cost = cost
        return self

    def set_payment(self, method: str) -> OrderBuilder:
        self._order.payment_method = method
        return self

    def apply_coupon(self, code: str, discount_pct: float) -> OrderBuilder:
        self._order.coupon_code = code
        self._order.discount_pct = discount_pct
        return self

    def add_decoration(self, decoration: str) -> OrderBuilder:
        self._order.decorations.append(decoration)
        return self

    def build(self) -> Order:
        discount = self._order.subtotal * (self._order.discount_pct / 100)
        self._order.total = round(
            self._order.subtotal - discount + self._order.delivery_cost, 2
        )
        return self._order


_orders_store: dict[str, dict] = {}


def save_order(order: Order) -> None:
    _orders_store[order.order_id] = order.to_dict()


def get_order(order_id: str) -> dict | None:
    return _orders_store.get(order_id)


def get_all_orders() -> list[dict]:
    return list(_orders_store.values())



COUPONS: dict[str, float] = {
    "SAVE10": 10.0,
    "SAVE20": 20.0,
    "HALFOFF": 50.0,
    "WELCOME": 5.0,
}


def validate_coupon(code: str) -> float:

    return COUPONS.get(code.upper(), 0.0)
