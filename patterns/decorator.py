from abc import ABC, abstractmethod
from typing import Optional

class Component(ABC):

    @abstractmethod
    def operation(self) -> str:

        ...

class ConcreteComponent(Component):

    def operation(self) -> str:

        return "ConcreteComponent"

class Decorator(Component):

    def __init__(self, component: Component):
        self._component = component  # ← Ссылка на компонент

    def operation(self) -> str:

        return self._component.operation()

class ConcreteDecoratorA(Decorator):

    def operation(self) -> str:

        component_result = self._component.operation()
        
        added_behavior = "ConcreteDecoratorA: addedBehavior()"
        
        return f"{component_result}{{{added_behavior}}}"
    
    def added_state(self) -> str:

        return "Added State from ConcreteDecoratorA"

class ConcreteDecoratorB(Decorator):

    def operation(self) -> str:

        component_result = self._component.operation()
        
        added_behavior = "Decorator::Operation() + addedBehavior()"
        
        return f"{component_result}[{added_behavior}]"
    
    def added_behavior(self) -> str:

        return "Added Behavior from ConcreteDecoratorB"

class OrderComponent(ABC):

    @abstractmethod
    def get_cost(self) -> float:

        ...

    @abstractmethod
    def get_description(self) -> str:

        ...

class BaseOrder(OrderComponent):

    def __init__(self, items: list[dict], delivery_cost: float = 0.0):
        self._subtotal = sum(i["price"] * i["quantity"] for i in items)
        self._delivery_cost = delivery_cost

    def get_cost(self) -> float:
        return round(self._subtotal + self._delivery_cost, 2)

    def get_description(self) -> str:
        return f"Заказ на сумму {self._subtotal:.2f} ₽ + доставка {self._delivery_cost:.2f} ₽"

class OrderDecorator(OrderComponent):

    def __init__(self, component: OrderComponent):
        self._component = component  # ← Ссылка на компонент

    def get_cost(self) -> float:

        return self._component.get_cost()

    def get_description(self) -> str:

        return self._component.get_description()

class GiftWrapDecorator(OrderDecorator):

    COST = 150.0

    def get_cost(self) -> float:

        return round(self._component.get_cost() + self.COST, 2)

    def get_description(self) -> str:

        return self._component.get_description() + " + 🎁 Подарочная упаковка"

class ExpressUpgradeDecorator(OrderDecorator):

    COST = 300.0

    def get_cost(self) -> float:

        return round(self._component.get_cost() + self.COST, 2)

    def get_description(self) -> str:

        return self._component.get_description() + " + ⚡ Ускоренная обработка"

class InsuranceDecorator(OrderDecorator):

    def __init__(self, component: OrderComponent):
        super().__init__(component)
        self._insurance_cost = max(50.0, round(component.get_cost() * 0.01, 2))

    def get_cost(self) -> float:

        return round(self._component.get_cost() + self._insurance_cost, 2)

    def get_description(self) -> str:

        return self._component.get_description() + f" + 🛡️ Страховка ({self._insurance_cost}₽)"

class DiscountDecorator(OrderDecorator):

    def __init__(self, component: OrderComponent, discount_pct: float):
        super().__init__(component)
        self._discount_pct = discount_pct

    def get_cost(self) -> float:

        base_cost = self._component.get_cost()
        return round(base_cost * (1 - self._discount_pct / 100), 2)

    def get_description(self) -> str:

        return self._component.get_description() + f" – 🏷️ Скидка {self._discount_pct:.0f}%"

def apply_decorators(
    base: OrderComponent,
    decorators: list[str],
    discount_pct: float = 0.0
) -> OrderComponent:

    
    result = base
    
    decorator_map = {
        "gift_wrap": GiftWrapDecorator,
        "express": ExpressUpgradeDecorator,
        "insurance": InsuranceDecorator,
    }
    
    for decorator_name in decorators:
        decorator_class = decorator_map.get(decorator_name)
        if decorator_class:
            result = decorator_class(result)  # ← Каждый новый декоратор оборачивает предыдущий
    
    if discount_pct > 0:
        result = DiscountDecorator(result, discount_pct)
    
    return result

def get_extras(decorated: OrderComponent) -> list[dict]:

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
