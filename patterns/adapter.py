from abc import ABC, abstractmethod


# ─────────────────────────────────────────────
#  ADAPTER  –  адаптер платёжных API
# ─────────────────────────────────────────────

# ── «Несовместимые» сторонние API ────────────

class StripeAPILegacy:
    """Имитация реального Stripe SDK (несовместимый интерфейс)."""

    def create_charge(self, amount_cents: int, currency: str, source_token: str) -> dict:
        return {
            "id": f"ch_stripe_{abs(hash(source_token)) % 100000}",
            "amount": amount_cents,
            "currency": currency,
            "status": "succeeded",
            "provider": "Stripe",
        }

    def refund_charge(self, charge_id: str) -> dict:
        return {"refund_id": f"re_{charge_id}", "status": "refunded"}


class PayPalSDKLegacy:
    """Имитация PayPal SDK (другой несовместимый интерфейс)."""

    def execute_payment(self, payer_id: str, amount: float) -> dict:
        return {
            "transaction_id": f"PAY-PP-{abs(hash(payer_id)) % 100000}",
            "amount": amount,
            "state": "approved",
            "provider": "PayPal",
        }

    def cancel_payment(self, transaction_id: str) -> dict:
        return {"transaction_id": transaction_id, "state": "cancelled"}


class YooKassaSDKLegacy:
    """Имитация ЮKassa SDK."""

    def init_payment(self, value: float, description: str) -> dict:
        return {
            "payment_id": f"YK-{abs(hash(description)) % 100000}",
            "amount": {"value": value, "currency": "RUB"},
            "status": "waiting_for_capture",
            "provider": "ЮKassa",
        }

    def capture_payment(self, payment_id: str) -> dict:
        return {"payment_id": payment_id, "status": "succeeded"}


# ── Единый интерфейс (целевой) ───────────────

class PaymentProcessor(ABC):
    """Единый интерфейс для всех платёжных адаптеров."""

    @abstractmethod
    def process_payment(self, amount: float, details: dict) -> dict: ...

    @abstractmethod
    def refund(self, transaction_id: str) -> dict: ...

    @abstractmethod
    def get_provider_name(self) -> str: ...


# ── Конкретные адаптеры ──────────────────────

class StripeAdapter(PaymentProcessor):
    def __init__(self):
        self._stripe = StripeAPILegacy()

    def process_payment(self, amount: float, details: dict) -> dict:
        result = self._stripe.create_charge(
            amount_cents=int(amount * 100),
            currency="rub",
            source_token=details.get("card_number", "tok_test"),
        )
        return {
            "success": result["status"] == "succeeded",
            "transaction_id": result["id"],
            "amount": amount,
            "provider": result["provider"],
        }

    def refund(self, transaction_id: str) -> dict:
        result = self._stripe.refund_charge(transaction_id)
        return {"success": result["status"] == "refunded", "refund_id": result["refund_id"]}

    def get_provider_name(self) -> str:
        return "Stripe"


class PayPalAdapter(PaymentProcessor):
    def __init__(self):
        self._paypal = PayPalSDKLegacy()

    def process_payment(self, amount: float, details: dict) -> dict:
        result = self._paypal.execute_payment(
            payer_id=details.get("paypal_email", "payer@example.com"),
            amount=amount,
        )
        return {
            "success": result["state"] == "approved",
            "transaction_id": result["transaction_id"],
            "amount": amount,
            "provider": result["provider"],
        }

    def refund(self, transaction_id: str) -> dict:
        result = self._paypal.cancel_payment(transaction_id)
        return {"success": result["state"] == "cancelled", "transaction_id": transaction_id}

    def get_provider_name(self) -> str:
        return "PayPal"


class YooKassaAdapter(PaymentProcessor):
    def __init__(self):
        self._yookassa = YooKassaSDKLegacy()

    def process_payment(self, amount: float, details: dict) -> dict:
        result = self._yookassa.init_payment(
            value=amount,
            description=details.get("description", "Заказ"),
        )
        captured = self._yookassa.capture_payment(result["payment_id"])
        return {
            "success": captured["status"] == "succeeded",
            "transaction_id": captured["payment_id"],
            "amount": amount,
            "provider": result["provider"],
        }

    def refund(self, transaction_id: str) -> dict:
        return {"success": True, "transaction_id": transaction_id, "note": "ЮKassa возврат инициирован"}

    def get_provider_name(self) -> str:
        return "ЮKassa"


# ── Реестр адаптеров ─────────────────────────

PAYMENT_ADAPTERS: dict[str, PaymentProcessor] = {
    "card": StripeAdapter(),
    "paypal": PayPalAdapter(),
    "crypto": YooKassaAdapter(),
}


def get_payment_adapter(method: str) -> PaymentProcessor:
    adapter = PAYMENT_ADAPTERS.get(method)
    if adapter is None:
        raise ValueError(f"Нет адаптера для: {method}")
    return adapter
