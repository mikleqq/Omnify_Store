from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar('T')

class Iterator(ABC, Generic[T]):
    
    @abstractmethod
    def first(self) -> T:
        ...
    
    @abstractmethod
    def next(self) -> T:
        ...
    
    @abstractmethod
    def is_done(self) -> bool:
        ...
    
    @abstractmethod
    def current_item(self) -> T:
        ...

class ProductIterator(Iterator):
    
    def __init__(self, products: list):
        self.products = products
        self.index = 0
    
    def first(self) -> Any:
        self.index = 0
        if len(self.products) > 0:
            return self.products[0]
        return None
    
    def next(self) -> Any:
        if self.index < len(self.products) - 1:
            self.index += 1
            return self.products[self.index]
        return None
    
    def is_done(self) -> bool:
    
        return self.index >= len(self.products) - 1
    
    def current_item(self) -> Any:
    
        if 0 <= self.index < len(self.products):
            return self.products[self.index]
        return None

class ReverseProductIterator(Iterator):

    
    def __init__(self, products: list):
        self.products = products
        self.index = len(products) - 1
    
    def first(self) -> Any:
    
        self.index = len(self.products) - 1
        if self.index >= 0:
            return self.products[self.index]
        return None
    
    def next(self) -> Any:
    
        if self.index > 0:
            self.index -= 1
            return self.products[self.index]
        return None
    
    def is_done(self) -> bool:
    
        return self.index <= 0
    
    def current_item(self) -> Any:
    
        if 0 <= self.index < len(self.products):
            return self.products[self.index]
        return None

class FilteredProductIterator(Iterator):

    
    def __init__(self, products: list, filter_func):
        self.products = [p for p in products if filter_func(p)]
        self.index = 0
    
    def first(self) -> Any:
    
        self.index = 0
        if len(self.products) > 0:
            return self.products[0]
        return None
    
    def next(self) -> Any:
    
        if self.index < len(self.products) - 1:
            self.index += 1
            return self.products[self.index]
        return None
    
    def is_done(self) -> bool:
    
        return self.index >= len(self.products) - 1
    
    def current_item(self) -> Any:
    
        if 0 <= self.index < len(self.products):
            return self.products[self.index]
        return None

class SortedProductIterator(Iterator):

    
    def __init__(self, products: list, sort_key=None, reverse: bool = False):
        self.products = sorted(products, key=sort_key, reverse=reverse)
        self.index = 0
    
    def first(self) -> Any:
    
        self.index = 0
        if len(self.products) > 0:
            return self.products[0]
        return None
    
    def next(self) -> Any:
    
        if self.index < len(self.products) - 1:
            self.index += 1
            return self.products[self.index]
        return None
    
    def is_done(self) -> bool:
    
        return self.index >= len(self.products) - 1
    
    def current_item(self) -> Any:
    
        if 0 <= self.index < len(self.products):
            return self.products[self.index]
        return None

class Aggregate(ABC):

    
    @abstractmethod
    def create_iterator(self) -> Iterator:
    
        ...

class ProductCatalog(Aggregate):

    
    def __init__(self, products: list = None):
        self.products = products or []
    
    def add_product(self, product: Any):
    
        self.products.append(product)
    
    def remove_product(self, product: Any):
    
        if product in self.products:
            self.products.remove(product)
    
    def create_iterator(self) -> Iterator:
    
        return ProductIterator(self.products)
    
    def create_reverse_iterator(self) -> Iterator:
    
        return ReverseProductIterator(self.products)
    
    def create_filtered_iterator(self, filter_func) -> Iterator:
    
        return FilteredProductIterator(self.products, filter_func)
    
    def create_sorted_iterator(self, sort_key=None, reverse: bool = False) -> Iterator:
    
        return SortedProductIterator(self.products, sort_key, reverse)
    
    def count(self) -> int:
    
        return len(self.products)

class CatalogClient:

    
    def __init__(self, catalog: ProductCatalog):
        self.catalog = catalog
    
    def print_catalog(self):
    
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

class PaginatedIterator(Iterator):

    
    def __init__(self, products: list, page_size: int = 10):
        self.products = products
        self.page_size = page_size
        self.current_page = 0
        self.index = 0
    
    def first(self) -> list:
    
        self.current_page = 0
        self.index = 0
        return self.get_page(0)
    
    def next(self) -> list:
    
        if self.current_page < self.get_total_pages() - 1:
            self.current_page += 1
            return self.get_page(self.current_page)
        return []
    
    def is_done(self) -> bool:
    
        return self.current_page >= self.get_total_pages() - 1
    
    def current_item(self) -> list:
    
        return self.get_page(self.current_page)
    
    def get_page(self, page_num: int) -> list:
    
        start = page_num * self.page_size
        end = start + self.page_size
        return self.products[start:end]
    
    def get_total_pages(self) -> int:
    
        return (len(self.products) + self.page_size - 1) // self.page_size

class PaginatedCatalog(Aggregate):

    
    def __init__(self, products: list = None, page_size: int = 10):
        self.products = products or []
        self.page_size = page_size
    
    def create_iterator(self) -> PaginatedIterator:
    
        return PaginatedIterator(self.products, self.page_size)
