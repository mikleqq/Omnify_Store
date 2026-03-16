from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field

@dataclass
class Position:

    row: int = 0
    col: int = 0

    def __str__(self) -> str:
        return f"[{self.row},{self.col}]"


# ═══════════════════════════════════════════════════════════════
#  PROTOTYPE HIERARCHY  (Graphic → ...)
# ═══════════════════════════════════════════════════════════════

class ProductCard(ABC):


    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    @abstractmethod
    def render(self, position: Position) -> str:
        """Draw(Position) из диаграммы."""
        ...

    def clone(self) -> "ProductCard":
    
        return deepcopy(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.product_id!r}, name={self.name!r})"


class BundleCard(ProductCard):


    def __init__(self, product_id: str, name: str, price: float,
                 items: list[str] | None = None):
        super().__init__(product_id, name, price)
        self.items: list[str] = items or []

    def render(self, position: Position) -> str:
        contents = ", ".join(self.items) if self.items else "—"
        return (
            f"[BundleCard] {position} | {self.name} "
            f"| ${self.price} | Состав: {contents}"
        )

    def clone(self) -> "BundleCard":
        copy = deepcopy(self)
        copy.product_id = self.product_id + "_copy"
        return copy


class LicensedCard(ProductCard, ABC):


    @abstractmethod
    def get_license_type(self) -> str: ...

    def render(self, position: Position) -> str:
        return (
            f"[{self.__class__.__name__}] {position} | {self.name} "
            f"| ${self.price} | Лицензия: {self.get_license_type()}"
        )


class FullLicense(LicensedCard):


    def get_license_type(self) -> str:
        return "Полная коммерческая"

    def clone(self) -> "FullLicense":
        copy = deepcopy(self)
        copy.product_id = self.product_id + "_copy"
        return copy


class TrialLicense(LicensedCard):
   

    def __init__(self, product_id: str, name: str, price: float,
                 trial_days: int = 14):
        super().__init__(product_id, name, price)
        self.trial_days = trial_days

    def get_license_type(self) -> str:
        return f"Пробная ({self.trial_days} дней)"

    def clone(self) -> "TrialLicense":
        copy = deepcopy(self)
        copy.product_id = self.product_id + "_copy"
        return copy


class CatalogTool(ABC):


    @abstractmethod
    def apply(self, drawing: list[ProductCard],
              position: Position | None = None) -> str:

        ...


class SortTool(CatalogTool):


    def apply(self, drawing: list[ProductCard],
              position: Position | None = None) -> str:
        drawing.sort(key=lambda c: c.price)
        names = [c.name for c in drawing]
        return f"[SortTool] Каталог отсортирован: {names}"


class QuickAddTool(CatalogTool):


    def __init__(self, prototype: ProductCard):
        self.prototype = prototype        # ← поле prototype из диаграммы

    def apply(self, drawing: list[ProductCard],
              position: Position | None = None) -> str:
        if position is None:
            position = Position(row=len(drawing), col=0)

        # 1. p = prototype->Clone()
        p = self.prototype.clone()

        # 2. while (пользователь тащит мышь) { p->Draw(new position) }
        log_lines: list[str] = []
        for col in range(3):                          # имитация 3 промежуточных позиций
            interim = Position(row=position.row, col=col)
            log_lines.append(p.render(interim))

        # 3. вставить p в рисунок (каталог)
        drawing.append(p)

        result = "\n  ".join(log_lines)
        return (
            f"[QuickAddTool] Прототип: {self.prototype!r}\n"
            f"  Клон создан: {p!r}\n"
            f"  Промежуточные позиции:\n  {result}\n"
            f"  Вставлен в каталог на позицию {position}"
        )


_PROTOTYPE_REGISTRY: dict[str, ProductCard] = {}


def register_prototype(card: ProductCard) -> None:

    _PROTOTYPE_REGISTRY[card.product_id] = card


def get_prototype(product_id: str) -> ProductCard | None:

    return _PROTOTYPE_REGISTRY.get(product_id)


def clone_product(product_id: str) -> ProductCard | None:

    proto = get_prototype(product_id)
    return proto.clone() if proto else None




register_prototype(BundleCard("b1",  "Набор геймера",          299,
                               ["Ноутбук ASUS ROG", "Мышь", "Наушники"]))
register_prototype(FullLicense("fl1", "Adobe CC (полная)",      599))
register_prototype(TrialLicense("tl1", "Adobe CC (trial)",      0, trial_days=30))
