from abc import ABC, abstractmethod
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
#  BRIDGE PATTERN
#  (Разделение абстракции от реализации)
#
#  Структура:
#    Client
#       ↓
#    Abstraction (Operation)
#       ├─ RefinedAbstraction
#       └─ [imp] Implementor (OperationImpl)
#              ├─ ConcreteImplementorA
#              └─ ConcreteImplementorB
# ═══════════════════════════════════════════════════════════════════════════

# ──── Implementor (Интерфейс реализации) ────────────────────────────────

class PaymentImplementor(ABC):
    """Интерфейс платёжной системы. Определяет контракт для всех способов оплаты."""

    @abstractmethod
    def authorize(self, amount: float, details: dict) -> dict:
        """Авторизовать платёж. Возвращает {success, transaction_id, ...}"""
        ...

    @abstractmethod
    def capture(self, transaction_id: str) -> dict:
        """Захватить (завершить) платёж."""
        ...

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> dict:
        """Сделать возврат денег."""
        ...

    @abstractmethod
    def get_name(self) -> str:
        """Получить имя способа оплаты."""
        ...


# ──── ConcreteImplementorA (Конкретная реализация A) ─────────────────────

class CreditCardPayment(PaymentImplementor):
    """Конкретная реализация платежа через кредитную карту."""

    def authorize(self, amount: float, details: dict) -> dict:
        """Авторизация платежа по карте."""
        card_number = details.get("card_number", "****")
        print(f"💳 CreditCard: Авторизация {amount}₽ на карту {card_number[-4:]}")
        return {
            "success": True,
            "transaction_id": f"CC-{abs(hash(card_number)) % 100000}",
            "status": "authorized",
            "amount": amount,
            "method": "credit_card",
        }

    def capture(self, transaction_id: str) -> dict:
        """Захватить авторизованный платёж."""
        print(f"💳 CreditCard: Захват платежа {transaction_id}")
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "captured",
        }

    def refund(self, transaction_id: str, amount: float) -> dict:
        """Вернуть деньги на карту."""
        print(f"💳 CreditCard: Возврат {amount}₽ на {transaction_id}")
        return {
            "success": True,
            "refund_id": f"RF-{transaction_id}",
            "amount": amount,
            "status": "refunded",
        }

    def get_name(self) -> str:
        return "Кредитная карта"


# ──── ConcreteImplementorB (Конкретная реализация B) ─────────────────────

class PayPalPayment(PaymentImplementor):
    """Конкретная реализация платежа через PayPal."""

    def authorize(self, amount: float, details: dict) -> dict:
        """Авторизация платежа через PayPal."""
        email = details.get("paypal_email", "user@paypal")
        print(f"🅿️  PayPal: Авторизация {amount}₽ на аккаунт {email}")
        return {
            "success": True,
            "transaction_id": f"PP-{abs(hash(email)) % 100000}",
            "status": "authorized",
            "amount": amount,
            "method": "paypal",
        }

    def capture(self, transaction_id: str) -> dict:
        """Захватить авторизованный платёж."""
        print(f"🅿️  PayPal: Захват платежа {transaction_id}")
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "captured",
        }

    def refund(self, transaction_id: str, amount: float) -> dict:
        """Вернуть деньги в PayPal аккаунт."""
        print(f"🅿️  PayPal: Возврат {amount}₽ на {transaction_id}")
        return {
            "success": True,
            "refund_id": f"RF-{transaction_id}",
            "amount": amount,
            "status": "refunded",
        }

    def get_name(self) -> str:
        return "PayPal"


# ──── ConcreteImplementorC (Конкретная реализация C) ────────────────────

class CryptoPayment(PaymentImplementor):
    """Конкретная реализация платежа через криптовалюту."""

    def authorize(self, amount: float, details: dict) -> dict:
        """Авторизация платежа через крипто."""
        wallet = details.get("crypto_wallet", "0x0000")
        print(f"₿  Crypto: Авторизация {amount}₽ на кошелёк {wallet[:8]}...")
        return {
            "success": True,
            "transaction_id": f"CR-{abs(hash(wallet)) % 100000}",
            "status": "authorized",
            "amount": amount,
            "method": "cryptocurrency",
        }

    def capture(self, transaction_id: str) -> dict:
        """Захватить авторизованный платёж."""
        print(f"₿  Crypto: Захват платежа {transaction_id}")
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "captured",
        }

    def refund(self, transaction_id: str, amount: float) -> dict:
        """Вернуть крипто."""
        print(f"₿  Crypto: Возврат {amount}₽ на {transaction_id}")
        return {
            "success": True,
            "refund_id": f"RF-{transaction_id}",
            "amount": amount,
            "status": "refunded",
        }

    def get_name(self) -> str:
        return "Криптовалюта"


# ───────────────────────────────────────────────────────────────────────────

# ──── Abstraction (Абстракция) ────────────────────────────────────────────

class OrderProcessor(ABC):
    """Абстракция для обработки заказов.
    
    Использует Bridge паттерн для разделения от способа оплаты.
    Содержит ссылку (bridge) на PaymentImplementor.
    """

    def __init__(self, payment: PaymentImplementor):
        self._payment = payment  # ← BRIDGE: связь с реализацией

    @abstractmethod
    def process(self, order_data: dict) -> dict:
        """Обработать заказ (разные стратегии для разных подклассов)."""
        ...

    def get_payment_method(self) -> str:
        """Получить имя способа оплаты."""
        return self._payment.get_name()


# ──── RefinedAbstraction A (Уточненная абстракция A) ──────────────────────

class StandardOrderProcessor(OrderProcessor):
    """Обработка стандартных заказов.
    
    Использует одну и ту же реализацию PaymentImplementor,
    но логика обработки отличается от PremiumOrderProcessor.
    """

    def process(self, order_data: dict) -> dict:
        """Обработка стандартного заказа."""
        print(f"\n📦 StandardOrderProcessor: Обработка заказа")
        print(f"   Способ оплаты: {self.get_payment_method()}")
        
        order_id = order_data.get("order_id")
        amount = order_data.get("amount")
        details = order_data.get("payment_details", {})
        
        # Шаг 1: Авторизация (через Bridge)
        auth_result = self._payment.authorize(amount, details)
        if not auth_result["success"]:
            return {"success": False, "error": "Authorization failed"}
        
        # Шаг 2: Захват (через Bridge)
        capture_result = self._payment.capture(auth_result["transaction_id"])
        if not capture_result["success"]:
            return {"success": False, "error": "Capture failed"}
        
        return {
            "success": True,
            "order_id": order_id,
            "processor_type": "Standard",
            "transaction_id": auth_result["transaction_id"],
            "amount": amount,
            "payment_method": self.get_payment_method(),
            "status": "completed",
        }


# ──── RefinedAbstraction B (Уточненная абстракция B) ──────────────────────

class PremiumOrderProcessor(OrderProcessor):
    """Обработка премиум заказов.
    
    Отличается логикой обработки: добавляет проверки, сохранение платежа и т.д.
    Использует ТУ ЖЕ PaymentImplementor, но по-другому.
    """

    def process(self, order_data: dict) -> dict:
        """Обработка премиум заказа с дополнительными проверками."""
        print(f"\n🌟 PremiumOrderProcessor: Обработка ПРЕМИУМ заказа")
        print(f"   Способ оплаты: {self.get_payment_method()}")
        
        order_id = order_data.get("order_id")
        amount = order_data.get("amount")
        details = order_data.get("payment_details", {})
        
        # Дополнительная проверка для премиум
        if amount < 100:
            print(f"   ⚠️  Премиум заказ должен быть >= 100₽")
            return {"success": False, "error": "Premium order minimum not met"}
        
        # Шаг 1: Авторизация (через Bridge)
        auth_result = self._payment.authorize(amount, details)
        if not auth_result["success"]:
            return {"success": False, "error": "Authorization failed"}
        
        # Шаг 2: Дополнительная проверка безопасности
        print(f"   🔒 Премиум: Проверка безопасности...")
        
        # Шаг 3: Захват с премиум логикой (через Bridge)
        capture_result = self._payment.capture(auth_result["transaction_id"])
        if not capture_result["success"]:
            return {"success": False, "error": "Capture failed"}
        
        # Шаг 4: Дополнительное сохранение платежа для истории
        print(f"   💾 Премиум: Сохранение платежа в профиль...")
        
        return {
            "success": True,
            "order_id": order_id,
            "processor_type": "Premium",
            "transaction_id": auth_result["transaction_id"],
            "amount": amount,
            "payment_method": self.get_payment_method(),
            "status": "completed",
            "premium_benefits": ["Free shipping", "Extended warranty", "Priority support"],
        }


# ──── Factory для создания процессоров ───────────────────────────────────

class ProcessorFactory:
    """Фабрика для создания процессоров заказов с нужным способом оплаты."""

    _payment_methods = {
        "card": CreditCardPayment(),
        "paypal": PayPalPayment(),
        "crypto": CryptoPayment(),
    }

    @classmethod
    def create_standard(cls, payment_method: str) -> StandardOrderProcessor:
        """Создать стандартный процессор с нужным способом оплаты."""
        payment = cls._payment_methods.get(payment_method)
        if not payment:
            raise ValueError(f"Unknown payment method: {payment_method}")
        return StandardOrderProcessor(payment)

    @classmethod
    def create_premium(cls, payment_method: str) -> PremiumOrderProcessor:
        """Создать премиум процессор с нужным способом оплаты."""
        payment = cls._payment_methods.get(payment_method)
        if not payment:
            raise ValueError(f"Unknown payment method: {payment_method}")
        return PremiumOrderProcessor(payment)

    @classmethod
    def get_available_payments(cls) -> list[str]:
        """Получить список доступных способов оплаты."""
        return list(cls._payment_methods.keys())
