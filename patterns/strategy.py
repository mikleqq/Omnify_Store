from abc import ABC, abstractmethod


# ─────────────────────────────────────────────
#  STRATEGY  –  стратегии доставки
# ─────────────────────────────────────────────

class DeliveryStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, weight_kg: float, distance_km: float) -> float: ...

    @abstractmethod
    def get_name(self) -> str: ...

    @abstractmethod
    def get_description(self) -> str: ...

    @abstractmethod
    def get_days(self) -> str: ...

    @abstractmethod
    def get_icon(self) -> str: ...


class CourierDelivery(DeliveryStrategy):
    def calculate_cost(self, weight_kg: float, distance_km: float) -> float:
        base = 2.0
        return round(base + weight_kg * 0.2 + distance_km * 0.005, 2)

    def get_name(self) -> str:
        return "courier"

    def get_description(self) -> str:
        return "Курьерская доставка до двери"

    def get_days(self) -> str:
        return "2–4 дня"

    def get_icon(self) -> str:
        return "🚚"


class PickupDelivery(DeliveryStrategy):
    def calculate_cost(self, weight_kg: float, distance_km: float) -> float:
        return 0.0  # Самовывоз бесплатен

    def get_name(self) -> str:
        return "pickup"

    def get_description(self) -> str:
        return "Самовывоз из пункта выдачи"

    def get_days(self) -> str:
        return "1–2 дня"

    def get_icon(self) -> str:
        return "🏪"


class ExpressDelivery(DeliveryStrategy):
    def calculate_cost(self, weight_kg: float, distance_km: float) -> float:
        base = 6.0
        return round(base + weight_kg * 0.5 + distance_km * 0.02, 2)

    def get_name(self) -> str:
        return "express"

    def get_description(self) -> str:
        return "Экспресс-доставка (день-в-день)"

    def get_days(self) -> str:
        return "1 день"

    def get_icon(self) -> str:
        return "⚡"


class PostDelivery(DeliveryStrategy):
    def calculate_cost(self, weight_kg: float, distance_km: float) -> float:
        base = 1.0
        return round(base + weight_kg * 0.1, 2)

    def get_name(self) -> str:
        return "post"

    def get_description(self) -> str:
        return "Почтовая доставка (Почта России)"

    def get_days(self) -> str:
        return "7–14 дней"

    def get_icon(self) -> str:
        return "📮"


# ── Реестр стратегий ─────────────────────────

DELIVERY_STRATEGIES: dict[str, DeliveryStrategy] = {
    "courier": CourierDelivery(),
    "pickup": PickupDelivery(),
    "express": ExpressDelivery(),
    "post": PostDelivery(),
}


def get_delivery_strategy(name: str) -> DeliveryStrategy:
    strategy = DELIVERY_STRATEGIES.get(name)
    if strategy is None:
        raise ValueError(f"Неизвестная стратегия доставки: {name}")
    return strategy


class DeliveryContext:
    """Контекст, использующий выбранную стратегию."""

    def __init__(self, strategy: DeliveryStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DeliveryStrategy) -> None:
        self._strategy = strategy

    def calculate(self, weight_kg: float = 1.0, distance_km: float = 10.0) -> float:
        return self._strategy.calculate_cost(weight_kg, distance_km)

    def info(self) -> dict:
        return {
            "name": self._strategy.get_name(),
            "description": self._strategy.get_description(),
            "days": self._strategy.get_days(),
            "icon": self._strategy.get_icon(),
        }
