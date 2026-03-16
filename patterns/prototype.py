from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field


# ─────────────────────────────────────────────────────────────────
#  PROTOTYPE  –  клонирование карточек товаров
#
#  Структура точно соответствует GoF UML:
#
#   Graphic  ◄────────────────── GraphicTool.prototype
#   ├── Staff
#   └── MusicalNote  (abstract)
#       ├── WholeNote
#       └── HalfNote
#
#  Tool  (abstract)
#  ├── RotateTool
#  └── GraphicTool  ──► prototype: Graphic
#
#  В контексте магазина:
#   Graphic      → ProductCard    (абстрактная карточка товара)
#   Staff        → BundleCard     (карточка набора/комплекта)
#   MusicalNote  → LicensedCard   (абстрактная лицензируемая карточка)
#   WholeNote    → FullLicense    (полная лицензия)
#   HalfNote     → TrialLicense   (пробная / trial-версия)
#   Tool         → CatalogTool    (абстрактный инструмент каталога)
#   RotateTool   → SortTool       (сортировка / перестановка карточек)
#   GraphicTool  → QuickAddTool   (быстрое клонирование → добавление в корзину)
# ─────────────────────────────────────────────────────────────────


@dataclass
class Position:
    """Позиция / «слот» отображения карточки в каталоге."""
    row: int = 0
    col: int = 0

    def __str__(self) -> str:
        return f"[{self.row},{self.col}]"


# ═══════════════════════════════════════════════════════════════
#  PROTOTYPE HIERARCHY  (Graphic → ...)
# ═══════════════════════════════════════════════════════════════

class ProductCard(ABC):
    """
    Graphic — абстрактный прототип карточки товара.
    Каждый конкретный класс умеет себя отрисовать (render)
    и вернуть глубокую копию самого себя (clone).
    """

    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    @abstractmethod
    def render(self, position: Position) -> str:
        """Draw(Position) из диаграммы."""
        ...

    def clone(self) -> "ProductCard":
        """Clone() — возвращает копию самого себя (глубокое копирование)."""
        return deepcopy(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.product_id!r}, name={self.name!r})"


# ── Staff ─────────────────────────────────────────────────────

class BundleCard(ProductCard):
    """
    Staff — карточка физического набора/комплекта товаров.
    Хранит список вложенных позиций.
    """

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


# ── MusicalNote (abstract) → LicensedCard ────────────────────

class LicensedCard(ProductCard, ABC):
    """
    MusicalNote — абстрактная карточка лицензируемого цифрового товара.
    Конкретные подклассы определяют тип лицензии.
    """

    @abstractmethod
    def get_license_type(self) -> str: ...

    def render(self, position: Position) -> str:
        return (
            f"[{self.__class__.__name__}] {position} | {self.name} "
            f"| ${self.price} | Лицензия: {self.get_license_type()}"
        )


class FullLicense(LicensedCard):
    """
    WholeNote — полная (коммерческая) лицензия.
    Clone() возвращает копию самого себя.
    """

    def get_license_type(self) -> str:
        return "Полная коммерческая"

    def clone(self) -> "FullLicense":
        copy = deepcopy(self)
        copy.product_id = self.product_id + "_copy"
        return copy


class TrialLicense(LicensedCard):
    """
    HalfNote — пробная (trial) лицензия, ограниченная по времени.
    Clone() возвращает копию самого себя.
    """

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


# ═══════════════════════════════════════════════════════════════
#  TOOL HIERARCHY  (Tool → RotateTool / GraphicTool)
# ═══════════════════════════════════════════════════════════════

class CatalogTool(ABC):
    """Tool — абстрактный инструмент работы с каталогом."""

    @abstractmethod
    def apply(self, drawing: list[ProductCard],
              position: Position | None = None) -> str:
        """Manipulate() из диаграммы."""
        ...


class SortTool(CatalogTool):
    """
    RotateTool — переставляет карточки в каталоге по цене.
    Не использует прототип; просто сортирует.
    """

    def apply(self, drawing: list[ProductCard],
              position: Position | None = None) -> str:
        drawing.sort(key=lambda c: c.price)
        names = [c.name for c in drawing]
        return f"[SortTool] Каталог отсортирован: {names}"


class QuickAddTool(CatalogTool):
    """
    GraphicTool — держит ссылку на прототип и при каждом apply():

        p = prototype.clone()          # ← Clone()
        while пользователь тащит мышь:
            p.render(new_position)     # ← Draw(Position)
        вставить p в каталог           # ← вставить p в рисунок
    """

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


# ═══════════════════════════════════════════════════════════════
#  Вспомогательная фабрика прототипов для маршрутов Flask
# ═══════════════════════════════════════════════════════════════

_PROTOTYPE_REGISTRY: dict[str, ProductCard] = {}


def register_prototype(card: ProductCard) -> None:
    """Зарегистрировать прототип по product_id."""
    _PROTOTYPE_REGISTRY[card.product_id] = card


def get_prototype(product_id: str) -> ProductCard | None:
    """Вернуть прототип по product_id (или None)."""
    return _PROTOTYPE_REGISTRY.get(product_id)


def clone_product(product_id: str) -> ProductCard | None:
    """Клонировать зарегистрированный прототип."""
    proto = get_prototype(product_id)
    return proto.clone() if proto else None


# ── Регистрируем прототипы по умолчанию ──────────────────────

register_prototype(BundleCard("b1",  "Набор геймера",          299,
                               ["Ноутбук ASUS ROG", "Мышь", "Наушники"]))
register_prototype(FullLicense("fl1", "Adobe CC (полная)",      599))
register_prototype(TrialLicense("tl1", "Adobe CC (trial)",      0, trial_days=30))
