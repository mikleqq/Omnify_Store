import threading


# ─────────────────────────────────────────────
#  SINGLETON  –  менеджер корзины пользователя
# ─────────────────────────────────────────────

class CartManager:
    """
    Singleton-менеджер корзин.
    Хранит все сессионные корзины (per-user) и гарантирует,
    что существует ровно один экземпляр менеджера.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._carts: dict[str, list] = {}
        return cls._instance

    # ── Работа с корзиной ────────────────────

    def get_cart(self, user_id: str) -> list:
        return self._carts.setdefault(user_id, [])

    def add_item(self, user_id: str, product_dict: dict) -> None:
        cart = self.get_cart(user_id)
        for item in cart:
            if item["product_id"] == product_dict["product_id"]:
                item["quantity"] += 1
                return
        product_dict["quantity"] = 1
        cart.append(product_dict)

    def remove_item(self, user_id: str, product_id: str) -> None:
        cart = self.get_cart(user_id)
        self._carts[user_id] = [i for i in cart if i["product_id"] != product_id]

    def update_quantity(self, user_id: str, product_id: str, quantity: int) -> None:
        cart = self.get_cart(user_id)
        for item in cart:
            if item["product_id"] == product_id:
                if quantity <= 0:
                    self.remove_item(user_id, product_id)
                else:
                    item["quantity"] = quantity
                return

    def clear_cart(self, user_id: str) -> None:
        self._carts[user_id] = []

    def cart_total(self, user_id: str) -> float:
        return sum(i["price"] * i["quantity"] for i in self.get_cart(user_id))

    def cart_count(self, user_id: str) -> int:
        return sum(i["quantity"] for i in self.get_cart(user_id))
