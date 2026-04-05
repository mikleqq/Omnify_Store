from abc import ABC, abstractmethod
from typing import Optional

class PaymentImplementor(ABC):

    @abstractmethod
    def authorize(self, amount: float, details: dict) -> dict:

        ...

    @abstractmethod
    def capture(self, transaction_id: str) -> dict:

        ...

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> dict:

        ...

    @abstractmethod
    def get_name(self) -> str:

        ...

class CreditCardPayment(PaymentImplementor):

    def authorize(self, amount: float, details: dict) -> dict:

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

        print(f"💳 CreditCard: Захват платежа {transaction_id}")
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "captured",
        }

    def refund(self, transaction_id: str, amount: float) -> dict:

        print(f"💳 CreditCard: Возврат {amount}₽ на {transaction_id}")
        return {
            "success": True,
            "refund_id": f"RF-{transaction_id}",
            "amount": amount,
            "status": "refunded",
        }

    def get_name(self) -> str:
        return "Кредитная карта"

class PayPalPayment(PaymentImplementor):

    def authorize(self, amount: float, details: dict) -> dict:

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

        print(f"🅿️  PayPal: Захват платежа {transaction_id}")
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "captured",
        }

    def refund(self, transaction_id: str, amount: float) -> dict:

        print(f"🅿️  PayPal: Возврат {amount}₽ на {transaction_id}")
        return {
            "success": True,
            "refund_id": f"RF-{transaction_id}",
            "amount": amount,
            "status": "refunded",
        }

    def get_name(self) -> str:
        return "PayPal"

class CryptoPayment(PaymentImplementor):

    def authorize(self, amount: float, details: dict) -> dict:

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

        print(f"₿  Crypto: Захват платежа {transaction_id}")
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "captured",
        }

    def refund(self, transaction_id: str, amount: float) -> dict:

        print(f"₿  Crypto: Возврат {amount}₽ на {transaction_id}")
        return {
            "success": True,
            "refund_id": f"RF-{transaction_id}",
            "amount": amount,
            "status": "refunded",
        }

    def get_name(self) -> str:
        return "Криптовалюта"

class OrderProcessor(ABC):

    def __init__(self, payment: PaymentImplementor):
        self._payment = payment  # ← BRIDGE: связь с реализацией

    @abstractmethod
    def process(self, order_data: dict) -> dict:

        ...

    def get_payment_method(self) -> str:

        return self._payment.get_name()

class StandardOrderProcessor(OrderProcessor):

    def process(self, order_data: dict) -> dict:

        print(f"\n📦 StandardOrderProcessor: Обработка заказа")
        print(f"   Способ оплаты: {self.get_payment_method()}")
        
        order_id = order_data.get("order_id")
        amount = order_data.get("amount")
        details = order_data.get("payment_details", {})
        
        auth_result = self._payment.authorize(amount, details)
        if not auth_result["success"]:
            return {"success": False, "error": "Authorization failed"}
        
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

class PremiumOrderProcessor(OrderProcessor):

    def process(self, order_data: dict) -> dict:

        print(f"\n🌟 PremiumOrderProcessor: Обработка ПРЕМИУМ заказа")
        print(f"   Способ оплаты: {self.get_payment_method()}")
        
        order_id = order_data.get("order_id")
        amount = order_data.get("amount")
        details = order_data.get("payment_details", {})
        
        if amount < 100:
            print(f"   ⚠️  Премиум заказ должен быть >= 100₽")
            return {"success": False, "error": "Premium order minimum not met"}
        
        auth_result = self._payment.authorize(amount, details)
        if not auth_result["success"]:
            return {"success": False, "error": "Authorization failed"}
        
        print(f"   🔒 Премиум: Проверка безопасности...")
        
        capture_result = self._payment.capture(auth_result["transaction_id"])
        if not capture_result["success"]:
            return {"success": False, "error": "Capture failed"}
        
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

class ProcessorFactory:

    _payment_methods = {
        "card": CreditCardPayment(),
        "paypal": PayPalPayment(),
        "crypto": CryptoPayment(),
    }

    @classmethod
    def create_standard(cls, payment_method: str) -> StandardOrderProcessor:

        payment = cls._payment_methods.get(payment_method)
        if not payment:
            raise ValueError(f"Unknown payment method: {payment_method}")
        return StandardOrderProcessor(payment)

    @classmethod
    def create_premium(cls, payment_method: str) -> PremiumOrderProcessor:

        payment = cls._payment_methods.get(payment_method)
        if not payment:
            raise ValueError(f"Unknown payment method: {payment_method}")
        return PremiumOrderProcessor(payment)

    @classmethod
    def get_available_payments(cls) -> list[str]:

        return list(cls._payment_methods.keys())
