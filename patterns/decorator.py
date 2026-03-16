from abc import ABC, abstractmethod


# ─────────────────────────────────────────────
#  DECORATOR  –  дополнительные опции заказа
# ─────────────────────────────────────────────

class OrderComponent(ABC):
    """Базовый компонент заказа."""

    @abstractmethod
    def get_total(self) -> float: ...

    @abstractmethod
    def get_description(self) -> str: ...

    @abstractmethod
    def get_extras(self) -> list[dict]: ...


class BaseOrder(OrderComponent):
    """Конкретный компонент – «голый» заказ без опций."""

    def __init__(self, items: list[dict], delivery_cost: float = 0.0):
        self._subtotal = sum(i["price"] * i["quantity"] for i in items)
        self._delivery_cost = delivery_cost

    def get_total(self) -> float:
        return round(self._subtotal + self._delivery_cost, 2)

    def get_description(self) -> str:
        return f"Заказ на сумму {self._subtotal:.2f} ₽ + доставка {self._delivery_cost:.2f} ₽"

    def get_extras(self) -> list[dict]:
        return []


class OrderDecorator(OrderComponent, ABC):
    """Абстрактный декоратор."""

    def __init__(self, component: OrderComponent):
        self._component = component

    def get_total(self) -> float:
        return self._component.get_total()

    def get_description(self) -> str:
        return self._component.get_description()

    def get_extras(self) -> list[dict]:
        return self._component.get_extras()


class GiftWrapDecorator(OrderDecorator):
    """Декоратор: подарочная упаковка (+150 ₽)."""

    COST = 150.0

    def get_total(self) -> float:
        return round(super().get_total() + self.COST, 2)

    def get_description(self) -> str:
        return super().get_description() + " + 🎁 Подарочная упаковка"

    def get_extras(self) -> list[dict]:
        return super().get_extras() + [{"name": "Подарочная упаковка", "icon": "🎁", "cost": self.COST}]


class DiscountDecorator(OrderDecorator):
    """Декоратор: скидка в процентах."""

    def __init__(self, component: OrderComponent, discount_pct: float):
        super().__init__(component)
        self._discount_pct = discount_pct

    def get_total(self) -> float:
        base = super().get_total()
        return round(base * (1 - self._discount_pct / 100), 2)

    def get_description(self) -> str:
        return super().get_description() + f" – 🏷️ Скидка {self._discount_pct:.0f}%"

    def get_extras(self) -> list[dict]:
        discount_amount = round(self._component.get_total() * self._discount_pct / 100, 2)
        return super().get_extras() + [
            {"name": f"Скидка {self._discount_pct:.0f}%", "icon": "🏷️", "cost": -discount_amount}
        ]


class ExpressUpgradeDecorator(OrderDecorator):
    """Декоратор: ускоренная обработка (+300 ₽)."""

    COST = 300.0

    def get_total(self) -> float:
        return round(super().get_total() + self.COST, 2)

    def get_description(self) -> str:
        return super().get_description() + " + ⚡ Ускоренная обработка"

    def get_extras(self) -> list[dict]:
        return super().get_extras() + [{"name": "Ускоренная обработка", "icon": "⚡", "cost": self.COST}]


class InsuranceDecorator(OrderDecorator):
    """Декоратор: страховка (1% от суммы, мин. 50 ₽)."""

    def __init__(self, component: OrderComponent):
        super().__init__(component)
        self._insurance_cost = max(50.0, round(component.get_total() * 0.01, 2))

    def get_total(self) -> float:
        return round(super().get_total() + self._insurance_cost, 2)

    def get_description(self) -> str:
        return super().get_description() + f" + 🛡️ Страховка"

    def get_extras(self) -> list[dict]:
        return super().get_extras() + [
            {"name": "Страховка груза", "icon": "🛡️", "cost": self._insurance_cost}
        ]


# ── Фабрика декораторов ──────────────────────

DECORATOR_MAP = {
    "gift_wrap": GiftWrapDecorator,
    "express_upgrade": ExpressUpgradeDecorator,
    "insurance": InsuranceDecorator,
}


def apply_decorators(base: OrderComponent, options: list[str], discount_pct: float = 0.0) -> OrderComponent:
    """Обернуть компонент в цепочку декораторов согласно списку опций."""
    result = base
    for opt in options:
        cls = DECORATOR_MAP.get(opt)
        if cls:
            result = cls(result)
    if discount_pct > 0:
        result = DiscountDecorator(result, discount_pct)
    return result
