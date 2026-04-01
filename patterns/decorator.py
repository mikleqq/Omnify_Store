from abc import ABC, abstractmethod
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
#  DECORATOR PATTERN
#  (Динамическое добавление функциональности к объектам)
#
#  Структура:
#    Component (интерфейс)
#    ├─ ConcreteComponent (базовая реализация)
#    └─ Decorator (обёртка)
#       ├─ contains: component → Component
#       └─ ConcreteDecorator (добавляет поведение)
# ═══════════════════════════════════════════════════════════════════════════

# ──── Component (Абстрактный компонент) ─────────────────────────────────

class Component(ABC):
    """Абстрактный компонент.
    
    Определяет интерфейс, который будут использовать
    как конкретные компоненты, так и декораторы.
    """

    @abstractmethod
    def operation(self) -> str:
        """Основная операция."""
        ...


# ──── ConcreteComponent (Конкретный компонент) ──────────────────────────

class ConcreteComponent(Component):
    """Конкретный компонент.
    
    Реализует базовую функциональность Operation().
    """

    def operation(self) -> str:
        """Возвращает базовое сообщение."""
        return "ConcreteComponent"


# ──── Decorator (Абстрактный декоратор) ────────────────────────────────

class Decorator(Component):
    """Абстрактный декоратор.
    
    Содержит ссылку на Component (которой может быть
    как конкретный компонент, так и другой декоратор).
    Реализует тот же интерфейс Component.
    """

    def __init__(self, component: Component):
        self._component = component  # ← Ссылка на компонент

    def operation(self) -> str:
        """Делегирует операцию хранящемуся компоненту."""
        return self._component.operation()


# ──── ConcreteDecoratorA (Конкретный декоратор A) ──────────────────────

class ConcreteDecoratorA(Decorator):
    """Конкретный декоратор A.
    
    Добавляет новое поведение к операции Operation().
    """

    def operation(self) -> str:
        """Вызывает операцию компонента и добавляет свою логику."""
        # 1. Вызовем операцию хранящегося компонента
        component_result = self._component.operation()
        
        # 2. Добавляем нашу дополнительную логику
        added_behavior = "ConcreteDecoratorA: addedBehavior()"
        
        # 3. Возвращаем объединённый результат
        return f"{component_result}{{{added_behavior}}}"
    
    def added_state(self) -> str:
        """Дополнительное состояние, доступное только в этом декораторе."""
        return "Added State from ConcreteDecoratorA"


# ──── ConcreteDecoratorB (Конкретный декоратор B) ──────────────────────

class ConcreteDecoratorB(Decorator):
    """Конкретный декоратор B.
    
    Добавляет ДРУГОЕ новое поведение к операции Operation().
    """

    def operation(self) -> str:
        """Вызывает операцию компонента и добавляет свою логику."""
        # 1. Вызовем операцию хранящегося компонента
        component_result = self._component.operation()
        
        # 2. Добавляем ДРУГУЮ дополнительную логику
        added_behavior = "Decorator::Operation() + addedBehavior()"
        
        # 3. Возвращаем объединённый результат
        return f"{component_result}[{added_behavior}]"
    
    def added_behavior(self) -> str:
        """Дополнительная логика, доступная только в этом декораторе."""
        return "Added Behavior from ConcreteDecoratorB"


# ═══════════════════════════════════════════════════════════════════════════
#  ПРИМЕНЕНИЕ: СИСТЕМА ЗАКАЗОВ С ОПЦИЯМИ
# ═══════════════════════════════════════════════════════════════════════════

# ──── Order System Components ────────────────────────────────────────────

class OrderComponent(ABC):
    """Интерфейс компонента заказа."""

    @abstractmethod
    def get_cost(self) -> float:
        """Получить стоимость."""
        ...

    @abstractmethod
    def get_description(self) -> str:
        """Получить описание."""
        ...


class BaseOrder(OrderComponent):
    """Конкретный компонент заказа."""

    def __init__(self, items: list[dict], delivery_cost: float = 0.0):
        self._subtotal = sum(i["price"] * i["quantity"] for i in items)
        self._delivery_cost = delivery_cost

    def get_cost(self) -> float:
        return round(self._subtotal + self._delivery_cost, 2)

    def get_description(self) -> str:
        return f"Заказ на сумму {self._subtotal:.2f} ₽ + доставка {self._delivery_cost:.2f} ₽"


class OrderDecorator(OrderComponent):
    """Абстрактный декоратор для заказа.
    
    Содержит ссылку на OrderComponent и добавляет функциональность.
    """

    def __init__(self, component: OrderComponent):
        self._component = component  # ← Ссылка на компонент

    def get_cost(self) -> float:
        """Делегирует получение стоимости компоненту."""
        return self._component.get_cost()

    def get_description(self) -> str:
        """Делегирует описание компоненту."""
        return self._component.get_description()


# ──── ConcreteDecoratorA: GiftWrap ──────────────────────────────────────

class GiftWrapDecorator(OrderDecorator):
    """Конкретный декоратор: Подарочная упаковка."""

    COST = 150.0

    def get_cost(self) -> float:
        """Добавляет стоимость упаковки."""
        return round(self._component.get_cost() + self.COST, 2)

    def get_description(self) -> str:
        """Добавляет описание упаковки."""
        return self._component.get_description() + " + 🎁 Подарочная упаковка"


# ──── ConcreteDecoratorB: Express ───────────────────────────────────────

class ExpressUpgradeDecorator(OrderDecorator):
    """Конкретный декоратор: Ускоренная доставка."""

    COST = 300.0

    def get_cost(self) -> float:
        """Добавляет стоимость ускоренной доставки."""
        return round(self._component.get_cost() + self.COST, 2)

    def get_description(self) -> str:
        """Добавляет описание ускоренной доставки."""
        return self._component.get_description() + " + ⚡ Ускоренная обработка"


# ──── ConcreteDecoratorC: Insurance ─────────────────────────────────────

class InsuranceDecorator(OrderDecorator):
    """Конкретный декоратор: Страховка груза."""

    def __init__(self, component: OrderComponent):
        super().__init__(component)
        self._insurance_cost = max(50.0, round(component.get_cost() * 0.01, 2))

    def get_cost(self) -> float:
        """Добавляет стоимость страховки."""
        return round(self._component.get_cost() + self._insurance_cost, 2)

    def get_description(self) -> str:
        """Добавляет описание страховки."""
        return self._component.get_description() + f" + 🛡️ Страховка ({self._insurance_cost}₽)"


# ──── ConcreteDecoratorD: Discount ──────────────────────────────────────

class DiscountDecorator(OrderDecorator):
    """Конкретный декоратор: Скидка."""

    def __init__(self, component: OrderComponent, discount_pct: float):
        super().__init__(component)
        self._discount_pct = discount_pct

    def get_cost(self) -> float:
        """Применяет скидку к стоимости."""
        base_cost = self._component.get_cost()
        return round(base_cost * (1 - self._discount_pct / 100), 2)

    def get_description(self) -> str:
        """Добавляет описание скидки."""
        return self._component.get_description() + f" – 🏷️ Скидка {self._discount_pct:.0f}%"


# ──── Фабрика декораторов ──────────────────────────────────────────────

def apply_decorators(
    base: OrderComponent,
    decorators: list[str],
    discount_pct: float = 0.0
) -> OrderComponent:
    """Применить декораторы к базовому заказу.
    
    Args:
        base: Базовый компонент заказа
        decorators: Список названий декораторов ("gift_wrap", "express", "insurance")
        discount_pct: Процент скидки (применяется последним)
    
    Returns:
        Декорированный заказ
    """
    
    # Используем эту переменную, чтобы наслаивать декораторы
    result = base
    
    # Карта доступных декораторов
    decorator_map = {
        "gift_wrap": GiftWrapDecorator,
        "express": ExpressUpgradeDecorator,
        "insurance": InsuranceDecorator,
    }
    
    # Применяем каждый запрошенный декоратор
    for decorator_name in decorators:
        decorator_class = decorator_map.get(decorator_name)
        if decorator_class:
            result = decorator_class(result)  # ← Каждый новый декоратор оборачивает предыдущий
    
    # Скидка применяется последней
    if discount_pct > 0:
        result = DiscountDecorator(result, discount_pct)
    
    return result


# ──── Вспомогательные функции для работы с декораторами ──────────────────

def get_extras(decorated: OrderComponent) -> list[dict]:
    """Получить список опций для декорированного заказа."""
    extras = []
    
    current = decorated
    while isinstance(current, OrderDecorator):
        if isinstance(current, GiftWrapDecorator):
            extras.append({
                "name": "Подарочная упаковка",
                "icon": "🎁",
                "cost": GiftWrapDecorator.COST
            })
        elif isinstance(current, ExpressUpgradeDecorator):
            extras.append({
                "name": "Ускоренная обработка",
                "icon": "⚡",
                "cost": ExpressUpgradeDecorator.COST
            })
        elif isinstance(current, InsuranceDecorator):
            extras.append({
                "name": "Страховка груза",
                "icon": "🛡️",
                "cost": current._insurance_cost
            })
        elif isinstance(current, DiscountDecorator):
            base_cost = current._component.get_cost()
            discount_amount = round(base_cost * current._discount_pct / 100, 2)
            extras.append({
                "name": f"Скидка {current._discount_pct:.0f}%",
                "icon": "🏷️",
                "cost": -discount_amount
            })
        
        current = current._component
    
    return extras
