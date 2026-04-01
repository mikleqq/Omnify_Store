from abc import ABC, abstractmethod
from typing import List, Optional


# ═══════════════════════════════════════════════════════════════════════════
#  COMPOSITE PATTERN
#  (Составление объектов в древовидные структуры)
#
#  Структура:
#    Client
#       ↓
#    Component
#    ├─ Operation()
#    ├─ Add(Component)
#    ├─ Remove(Component)
#    └─ GetChild(int)
#       │
#       ├─ Leaf (Operation())
#       │
#       └─ Composite (все методы)
#              └─ для всех потомков: g.Operation()
# ═══════════════════════════════════════════════════════════════════════════

# ──── Component (Абстрактный компонент) ─────────────────────────────────

class ProductComponent(ABC):
    """Абстрактный компонент иерархии товаров.
    
    Определяет единый интерфейс как для листьев (товары),
    так и для контейнеров (категории).
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_price(self) -> float:
        """Получить цену. Для листа - цена товара, для композита - сумма цен."""
        ...

    @abstractmethod
    def get_quantity(self) -> int:
        """Получить количество товаров. Для листа - 1, для композита - сумма."""
        ...

    @abstractmethod
    def get_description(self) -> str:
        """Получить описание товара/категории."""
        ...

    @abstractmethod
    def add(self, component: "ProductComponent") -> None:
        """Добавить дочерний компонент. Для листа - не поддерживается."""
        ...

    @abstractmethod
    def remove(self, component: "ProductComponent") -> None:
        """Удалить дочерний компонент. Для листа - не поддерживается."""
        ...

    @abstractmethod
    def get_child(self, index: int) -> Optional["ProductComponent"]:
        """Получить дочерний компонент по индексу."""
        ...

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Вывести дерево структуры с отступами."""
        ...


# ──── Leaf (Лист – конкретный товар) ────────────────────────────────────

class Product(ProductComponent):
    """Лист иерархии – конкретный товар.
    
    Не имеет дочерних компонентов.
    Реализует базовую операцию для одного товара.
    """

    def __init__(self, name: str, price: float, product_id: str = ""):
        super().__init__(name)
        self.price = price
        self.product_id = product_id or name.lower().replace(" ", "_")

    def get_price(self) -> float:
        """Цена товара."""
        return self.price

    def get_quantity(self) -> int:
        """Количество = 1 (это одиночный товар)."""
        return 1

    def get_description(self) -> str:
        """Описание товара."""
        return f"📦 {self.name} (${self.price:.2f})"

    def add(self, component: ProductComponent) -> None:
        """Товар не может содержать другие товары."""
        raise ValueError(f"Cannot add component to product '{self.name}'")

    def remove(self, component: ProductComponent) -> None:
        """Товар не может содержать другие товары."""
        raise ValueError(f"Cannot remove component from product '{self.name}'")

    def get_child(self, index: int) -> Optional[ProductComponent]:
        """Товар не имеет дочерних компонентов."""
        return None

    def display(self, indent: int = 0) -> str:
        """Вывести товар с отступом."""
        return " " * indent + f"📦 {self.name}: ${self.price:.2f}\n"


# ──── Composite (Контейнер – категория товаров) ──────────────────────────

class Category(ProductComponent):
    """Composite (контейнер) иерархии – категория товаров или подкатегория.
    
    Может содержать товары и другие категории.
    Реализует операции над всеми дочерними компонентами.
    """

    def __init__(self, name: str, category_id: str = ""):
        super().__init__(name)
        self.category_id = category_id or name.lower().replace(" ", "_")
        self.children: List[ProductComponent] = []

    def get_price(self) -> float:
        """Сумма цен всех дочерних компонентов."""
        total = 0.0
        for child in self.children:
            total += child.get_price()  # ← Рекурсивно вызывает get_price()
        return total

    def get_quantity(self) -> int:
        """Сумма количеств всех дочерних компонентов."""
        total = 0
        for child in self.children:
            total += child.get_quantity()  # ← Рекурсивно вызывает get_quantity()
        return total

    def get_description(self) -> str:
        """Описание категории с количеством товаров."""
        count = len(self.children)
        return f"📂 {self.name} ({count} item{'s' if count != 1 else ''})"

    def add(self, component: ProductComponent) -> None:
        """Добавить товар или подкатегорию в эту категорию."""
        if component not in self.children:
            self.children.append(component)

    def remove(self, component: ProductComponent) -> None:
        """Удалить товар или подкатегорию из этой категории."""
        if component in self.children:
            self.children.remove(component)

    def get_child(self, index: int) -> Optional[ProductComponent]:
        """Получить дочерний компонент по индексу."""
        if 0 <= index < len(self.children):
            return self.children[index]
        return None

    def display(self, indent: int = 0) -> str:
        """Вывести дерево иерархии с отступами.
        
        Рекурсивно вызывает display() для всех дочерних компонентов.
        """
        result = " " * indent + f"📂 {self.name}/\n"
        for child in self.children:
            result += child.display(indent + 2)  # ← Рекурсивный вызов
        return result

    def get_categories(self) -> List["Category"]:
        """Получить все подкатегории."""
        return [c for c in self.children if isinstance(c, Category)]

    def get_products(self) -> List[Product]:
        """Получить все товары в этой категории (не в подкатегориях)."""
        return [p for p in self.children if isinstance(p, Product)]

    def get_all_products_recursive(self) -> List[Product]:
        """Получить все товары рекурсивно (включая подкатегории)."""
        products = self.get_products()
        for category in self.get_categories():
            products.extend(category.get_all_products_recursive())  # ← Рекурсия
        return products


# ──── Store Catalog Builder (Вспомогательный класс) ──────────────────────

class StoreCatalog:
    """Построитель каталога товаров с иерархией категорий."""

    @staticmethod
    def build_sample_catalog() -> Category:
        """Создать пример каталога с категориями и товарами."""
        
        # Корневая категория
        root = Category("Electronics Store", "store")
        
        # Уровень 1: Основные категории
        smartphones = Category("Smartphones", "smartphones")
        laptops = Category("Laptops", "laptops")
        accessories = Category("Accessories", "accessories")
        
        root.add(smartphones)
        root.add(laptops)
        root.add(accessories)
        
        # Уровень 2: Подкатегории
        flagship = Category("Flagship Phones", "flagship_phones")
        budget = Category("Budget Phones", "budget_phones")
        
        smartphones.add(flagship)
        smartphones.add(budget)
        
        gaming = Category("Gaming Laptops", "gaming_laptops")
        ultrabook = Category("Ultrabooks", "ultrabooks")
        
        laptops.add(gaming)
        laptops.add(ultrabook)
        
        # Уровень 3: Товары (Листья)
        # Flagship phones
        flagship.add(Product("iPhone 15 Pro Max", 1199.99, "iphone15pm"))
        flagship.add(Product("Samsung Galaxy S24 Ultra", 1299.99, "s24ultra"))
        flagship.add(Product("OnePlus 12", 899.99, "oneplus12"))
        
        # Budget phones
        budget.add(Product("Poco X6 Pro", 299.99, "pocox6"))
        budget.add(Product("Redmi Note 13", 199.99, "redminote13"))
        
        # Gaming laptops
        gaming.add(Product("ROG Zephyrus G16", 2499.99, "rogi16"))
        gaming.add(Product("Predator Triton 500", 2199.99, "predator500"))
        
        # Ultrabooks
        ultrabook.add(Product("MacBook Air M3", 1299.99, "mbair"))
        ultrabook.add(Product("ThinkPad X1 Carbon", 1799.99, "x1carbon"))
        
        # Accessories (без подкатегорий)
        accessories.add(Product("Apple AirPods Pro", 249.99, "airpodspro"))
        accessories.add(Product("Sony WH-1000XM5 Headphones", 399.99, "sonymx5"))
        accessories.add(Product("USB-C Cable", 19.99, "usbccable"))
        accessories.add(Product("Laptop Stand", 49.99, "lapstand"))
        
        return root


# ──── Statistics Analysis (Анализ статистики) ───────────────────────────

class CatalogStatistics:
    """Анализатор статистики каталога."""

    @staticmethod
    def get_statistics(component: ProductComponent) -> dict:
        """Получить статистику для компонента и всех его потомков."""
        return {
            "name": component.name,
            "total_price": component.get_price(),
            "total_items": component.get_quantity(),
            "description": component.get_description(),
        }

    @staticmethod
    def get_price_distribution(category: Category) -> dict:
        """Получить распределение цен по подкатегориям."""
        distribution = {}
        for child in category.children:
            if isinstance(child, Category):
                distribution[child.name] = child.get_price()
            elif isinstance(child, Product):
                distribution[child.name] = child.get_price()
        return distribution

    @staticmethod
    def get_expensive_products(category: Category, min_price: float) -> List[Product]:
        """Получить все товары дороже указанной цены."""
        expensive = []
        for product in category.get_all_products_recursive():
            if product.get_price() >= min_price:
                expensive.append(product)
        return expensive

    @staticmethod
    def filter_by_price_range(category: Category, min_price: float, 
                              max_price: float) -> List[Product]:
        """Получить товары в диапазоне цен."""
        filtered = []
        for product in category.get_all_products_recursive():
            price = product.get_price()
            if min_price <= price <= max_price:
                filtered.append(product)
        return filtered
