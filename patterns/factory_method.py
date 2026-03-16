from abc import ABC, abstractmethod
from copy import deepcopy


# ─────────────────────────────────────────────
#  FACTORY METHOD  –  создание типов товаров
# ─────────────────────────────────────────────

class Product(ABC):
    """Базовый продукт."""

    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = 1

    @abstractmethod
    def get_type(self) -> str: ...

    @abstractmethod
    def get_icon(self) -> str: ...

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "type": self.get_type(),
            "icon": self.get_icon(),
        }


class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, weight_kg: float = 0.5):
        super().__init__(product_id, name, price)
        self.weight_kg = weight_kg

    def get_type(self) -> str:
        return "physical"

    def get_icon(self) -> str:
        return "📦"

    def to_dict(self):
        d = super().to_dict()
        d["weight_kg"] = self.weight_kg
        return d


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, download_url: str = "#"):
        super().__init__(product_id, name, price)
        self.download_url = download_url

    def get_type(self) -> str:
        return "digital"

    def get_icon(self) -> str:
        return "💾"

    def to_dict(self):
        d = super().to_dict()
        d["download_url"] = self.download_url
        return d


class SubscriptionProduct(Product):
    def __init__(self, product_id, name, price, period_days: int = 30):
        super().__init__(product_id, name, price)
        self.period_days = period_days

    def get_type(self) -> str:
        return "subscription"

    def get_icon(self) -> str:
        return "🔄"

    def to_dict(self):
        d = super().to_dict()
        d["period_days"] = self.period_days
        return d


class ProductFactory:
    """Factory Method: создаёт нужный тип товара по строковому ключу."""

    _registry = {
        "physical": PhysicalProduct,
        "digital": DigitalProduct,
        "subscription": SubscriptionProduct,
    }

    @classmethod
    def create(cls, kind: str, product_id: str, name: str, price: float, **kwargs) -> Product:
        creator = cls._registry.get(kind)
        if creator is None:
            raise ValueError(f"Неизвестный тип товара: {kind}")
        return creator(product_id, name, price, **kwargs)


# ─────────────────────────────────────────────
#  PROTOTYPE  –  клонирование товара в корзине
# ─────────────────────────────────────────────

class CloneableMixin:
    """Примесь Prototype: глубокое копирование объекта."""

    def clone(self):
        return deepcopy(self)


class CloneableProduct(CloneableMixin, PhysicalProduct):
    pass


class CloneableDigitalProduct(CloneableMixin, DigitalProduct):
    pass


class CloneableSubscriptionProduct(CloneableMixin, SubscriptionProduct):
    pass


CLONEABLE_MAP = {
    "physical": CloneableProduct,
    "digital": CloneableDigitalProduct,
    "subscription": CloneableSubscriptionProduct,
}


def create_cloneable_product(kind: str, product_id: str, name: str, price: float, **kwargs):
    cls = CLONEABLE_MAP.get(kind, CloneableProduct)
    return cls(product_id, name, price, **kwargs)
