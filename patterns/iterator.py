# ─────────────────────────────────────────────
#  ITERATOR  –  итератор для коллекций
# ─────────────────────────────────────────────
#
#  Структура:
#  - Iterator (интерфейс для доступа и обхода элементов)
#  - ConcreteIterator (реализует методы для обхода)
#  - Aggregate (интерфейс для создания итератора)
#  - ConcreteAggregate (создает ConcreteIterator)
#  - Client (использует Aggregate и Iterator)
#

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


T = TypeVar('T')


# ── ITERATOR ─────────────────────────────────

class Iterator(ABC, Generic[T]):
    """
    Iterator - интерфейс итератора
    Определяет интерфейс для доступа и обхода элементов агрегата
    """
    
    @abstractmethod
    def first(self) -> T:
        """First() - возвращает первый элемент"""
        ...
    
    @abstractmethod
    def next(self) -> T:
        """Next() - возвращает следующий элемент"""
        ...
    
    @abstractmethod
    def is_done(self) -> bool:
        """IsDone() - проверяет, закончился ли обход"""
        ...
    
    @abstractmethod
    def current_item(self) -> T:
        """CurrentItem() - возвращает текущий элемент"""
        ...


# ── CONCRETE ITERATOR ────────────────────────

class ProductIterator(Iterator):
    """
    ConcreteIterator - конкретный итератор
    Реализует интерфейс Iterator и следит за текущей позицией при обходе
    """
    
    def __init__(self, products: list):
        self.products = products
        self.index = 0
    
    def first(self) -> Any:
        """First() - возвращает первый элемент"""
        self.index = 0
        if len(self.products) > 0:
            return self.products[0]
        return None
    
    def next(self) -> Any:
        """Next() - возвращает следующий элемент"""
        if self.index < len(self.products) - 1:
            self.index += 1
            return self.products[self.index]
        return None
    
    def is_done(self) -> bool:
        """IsDone() - проверяет, закончился ли обход"""
        return self.index >= len(self.products) - 1
    
    def current_item(self) -> Any:
        """CurrentItem() - возвращает текущий элемент"""
        if 0 <= self.index < len(self.products):
            return self.products[self.index]
        return None


class ReverseProductIterator(Iterator):
    """
    ConcreteIterator - конкретный итератор в обратном порядке
    Реализует обход в обратном направлении
    """
    
    def __init__(self, products: list):
        self.products = products
        self.index = len(products) - 1
    
    def first(self) -> Any:
        """First() - возвращает первый элемент (последний в списке)"""
        self.index = len(self.products) - 1
        if self.index >= 0:
            return self.products[self.index]
        return None
    
    def next(self) -> Any:
        """Next() - возвращает следующий элемент (в обратном порядке)"""
        if self.index > 0:
            self.index -= 1
            return self.products[self.index]
        return None
    
    def is_done(self) -> bool:
        """IsDone() - проверяет, закончился ли обход"""
        return self.index <= 0
    
    def current_item(self) -> Any:
        """CurrentItem() - возвращает текущий элемент"""
        if 0 <= self.index < len(self.products):
            return self.products[self.index]
        return None


class FilteredProductIterator(Iterator):
    """
    ConcreteIterator - конкретный итератор с фильтром
    Обходит только элементы, соответствующие условию фильтра
    """
    
    def __init__(self, products: list, filter_func):
        self.products = [p for p in products if filter_func(p)]
        self.index = 0
    
    def first(self) -> Any:
        """First() - возвращает первый отфильтрованный элемент"""
        self.index = 0
        if len(self.products) > 0:
            return self.products[0]
        return None
    
    def next(self) -> Any:
        """Next() - возвращает следующий отфильтрованный элемент"""
        if self.index < len(self.products) - 1:
            self.index += 1
            return self.products[self.index]
        return None
    
    def is_done(self) -> bool:
        """IsDone() - проверяет, закончился ли обход"""
        return self.index >= len(self.products) - 1
    
    def current_item(self) -> Any:
        """CurrentItem() - возвращает текущий отфильтрованный элемент"""
        if 0 <= self.index < len(self.products):
            return self.products[self.index]
        return None


class SortedProductIterator(Iterator):
    """
    ConcreteIterator - конкретный итератор с сортировкой
    Обходит отсортированные элементы
    """
    
    def __init__(self, products: list, sort_key=None, reverse: bool = False):
        self.products = sorted(products, key=sort_key, reverse=reverse)
        self.index = 0
    
    def first(self) -> Any:
        """First() - возвращает первый отсортированный элемент"""
        self.index = 0
        if len(self.products) > 0:
            return self.products[0]
        return None
    
    def next(self) -> Any:
        """Next() - возвращает следующий отсортированный элемент"""
        if self.index < len(self.products) - 1:
            self.index += 1
            return self.products[self.index]
        return None
    
    def is_done(self) -> bool:
        """IsDone() - проверяет, закончился ли обход"""
        return self.index >= len(self.products) - 1
    
    def current_item(self) -> Any:
        """CurrentItem() - возвращает текущий отсортированный элемент"""
        if 0 <= self.index < len(self.products):
            return self.products[self.index]
        return None


# ── AGGREGATE ────────────────────────────────

class Aggregate(ABC):
    """
    Aggregate - интерфейс агрегата
    Определяет интерфейс для создания объекта-итератора
    """
    
    @abstractmethod
    def create_iterator(self) -> Iterator:
        """CreateIterator() - создает итератор"""
        ...


# ── CONCRETE AGGREGATE ───────────────────────

class ProductCatalog(Aggregate):
    """
    ConcreteAggregate - конкретный агрегат
    Реализует интерфейс создания итератора (CreateIterator())
    и возвращает ConcreteIterator
    """
    
    def __init__(self, products: list = None):
        self.products = products or []
    
    def add_product(self, product: Any):
        """Добавляет товар в каталог"""
        self.products.append(product)
    
    def remove_product(self, product: Any):
        """Удаляет товар из каталога"""
        if product in self.products:
            self.products.remove(product)
    
    def create_iterator(self) -> Iterator:
        """CreateIterator() - создает обычный итератор"""
        return ProductIterator(self.products)
    
    def create_reverse_iterator(self) -> Iterator:
        """CreateIterator() - создает итератор в обратном порядке"""
        return ReverseProductIterator(self.products)
    
    def create_filtered_iterator(self, filter_func) -> Iterator:
        """CreateIterator() - создает итератор с фильтром"""
        return FilteredProductIterator(self.products, filter_func)
    
    def create_sorted_iterator(self, sort_key=None, reverse: bool = False) -> Iterator:
        """CreateIterator() - создает отсортированный итератор"""
        return SortedProductIterator(self.products, sort_key, reverse)
    
    def count(self) -> int:
        """Возвращает количество товаров"""
        return len(self.products)


# ── CLIENT ───────────────────────────────────

class CatalogClient:
    """
    Client - клиент
    Использует Aggregate и Iterator для обхода элементов
    """
    
    def __init__(self, catalog: ProductCatalog):
        self.catalog = catalog
    
    def print_catalog(self):
        """Выводит весь каталог"""
        iterator = self.catalog.create_iterator()
        
        print("=== Каталог товаров ===")
        first_item = iterator.first()
        if first_item:
            print(f"  {first_item}")
        
        while not iterator.is_done():
            item = iterator.next()
            if item:
                print(f"  {item}")
    
    def print_reverse_catalog(self):
        """Выводит каталог в обратном порядке"""
        iterator = self.catalog.create_reverse_iterator()
        
        print("=== Каталог товаров (в обратном порядке) ===")
        first_item = iterator.first()
        if first_item:
            print(f"  {first_item}")
        
        while not iterator.is_done():
            item = iterator.next()
            if item:
                print(f"  {item}")
    
    def print_filtered_catalog(self, filter_func, label: str = "Отфильтрованные товары"):
        """Выводит отфильтрованный каталог"""
        iterator = self.catalog.create_filtered_iterator(filter_func)
        
        print(f"=== {label} ===")
        first_item = iterator.first()
        if first_item:
            print(f"  {first_item}")
        
        while not iterator.is_done():
            item = iterator.next()
            if item:
                print(f"  {item}")
    
    def print_sorted_catalog(self, sort_key=None, reverse: bool = False, label: str = "Отсортированные товары"):
        """Выводит отсортированный каталог"""
        iterator = self.catalog.create_sorted_iterator(sort_key, reverse)
        
        print(f"=== {label} ===")
        first_item = iterator.first()
        if first_item:
            print(f"  {first_item}")
        
        while not iterator.is_done():
            item = iterator.next()
            if item:
                print(f"  {item}")
    
    def collect_all(self) -> list:
        """Собирает все элементы в список"""
        iterator = self.catalog.create_iterator()
        items = []
        
        first_item = iterator.first()
        if first_item:
            items.append(first_item)
        
        while not iterator.is_done():
            item = iterator.next()
            if item:
                items.append(item)
        
        return items


# ── PAGINATED ITERATOR ───────────────────────

class PaginatedIterator(Iterator):
    """
    ConcreteIterator - конкретный итератор с постраничной навигацией
    """
    
    def __init__(self, products: list, page_size: int = 10):
        self.products = products
        self.page_size = page_size
        self.current_page = 0
        self.index = 0
    
    def first(self) -> list:
        """First() - возвращает первую страницу"""
        self.current_page = 0
        self.index = 0
        return self.get_page(0)
    
    def next(self) -> list:
        """Next() - возвращает следующую страницу"""
        if self.current_page < self.get_total_pages() - 1:
            self.current_page += 1
            return self.get_page(self.current_page)
        return []
    
    def is_done(self) -> bool:
        """IsDone() - проверяет, на последней ли странице"""
        return self.current_page >= self.get_total_pages() - 1
    
    def current_item(self) -> list:
        """CurrentItem() - возвращает текущую страницу"""
        return self.get_page(self.current_page)
    
    def get_page(self, page_num: int) -> list:
        """Возвращает конкретную страницу"""
        start = page_num * self.page_size
        end = start + self.page_size
        return self.products[start:end]
    
    def get_total_pages(self) -> int:
        """Возвращает общее количество страниц"""
        return (len(self.products) + self.page_size - 1) // self.page_size


class PaginatedCatalog(Aggregate):
    """
    ConcreteAggregate - каталог с постраничной навигацией
    """
    
    def __init__(self, products: list = None, page_size: int = 10):
        self.products = products or []
        self.page_size = page_size
    
    def create_iterator(self) -> PaginatedIterator:
        """CreateIterator() - создает постраничный итератор"""
        return PaginatedIterator(self.products, self.page_size)
