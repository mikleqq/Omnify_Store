from abc import ABC, abstractmethod


# ─────────────────────────────────────────────
#  ABSTRACT FACTORY  –  платёжные фабрики
# ─────────────────────────────────────────────

class PaymentButton(ABC):
    @abstractmethod
    def render(self) -> str: ...


class PaymentForm(ABC):
    @abstractmethod
    def render(self) -> str: ...


class PaymentFactory(ABC):
    """Абстрактная фабрика UI-компонентов для платёжной системы."""

    @abstractmethod
    def create_button(self) -> PaymentButton: ...

    @abstractmethod
    def create_form(self) -> PaymentForm: ...

    @abstractmethod
    def get_name(self) -> str: ...

    @abstractmethod
    def get_icon(self) -> str: ...


# ── PayPal ──────────────────────────────────

class PayPalButton(PaymentButton):
    def render(self) -> str:
        return '<button class="btn btn-paypal">💳 Оплатить через PayPal</button>'


class PayPalForm(PaymentForm):
    def render(self) -> str:
        return (
            '<div class="payment-form paypal-form">'
            '<input type="email" name="paypal_email" placeholder="Email PayPal" class="form-control mb-2">'
            '<input type="password" name="paypal_password" placeholder="Пароль PayPal" class="form-control">'
            '</div>'
        )


class PayPalFactory(PaymentFactory):
    def create_button(self) -> PaymentButton:
        return PayPalButton()

    def create_form(self) -> PaymentForm:
        return PayPalForm()

    def get_name(self) -> str:
        return "PayPal"

    def get_icon(self) -> str:
        return "🅿️"


# ── Bank Card ────────────────────────────────

class BankCardButton(PaymentButton):
    def render(self) -> str:
        return '<button class="btn btn-card">💳 Оплатить картой</button>'


class BankCardForm(PaymentForm):
    def render(self) -> str:
        return (
            '<div class="payment-form card-form">'
            '<input type="text" name="card_number" placeholder="Номер карты" class="form-control mb-2" maxlength="19">'
            '<div class="d-flex gap-2">'
            '<input type="text" name="card_expiry" placeholder="ММ/ГГ" class="form-control mb-2">'
            '<input type="text" name="card_cvv" placeholder="CVV" class="form-control mb-2" maxlength="3">'
            '</div>'
            '<input type="text" name="card_holder" placeholder="Имя держателя" class="form-control">'
            '</div>'
        )


class BankCardFactory(PaymentFactory):
    def create_button(self) -> PaymentButton:
        return BankCardButton()

    def create_form(self) -> PaymentForm:
        return BankCardForm()

    def get_name(self) -> str:
        return "Банковская карта"

    def get_icon(self) -> str:
        return "💳"


# ── Crypto (бонусная фабрика) ────────────────

class CryptoButton(PaymentButton):
    def render(self) -> str:
        return '<button class="btn btn-crypto">₿ Оплатить криптовалютой</button>'


class CryptoForm(PaymentForm):
    def render(self) -> str:
        return (
            '<div class="payment-form crypto-form">'
            '<input type="text" name="wallet" placeholder="Адрес кошелька" class="form-control mb-2">'
            '<select name="currency" class="form-select">'
            '<option value="BTC">Bitcoin (BTC)</option>'
            '<option value="ETH">Ethereum (ETH)</option>'
            '<option value="USDT">Tether (USDT)</option>'
            '</select>'
            '</div>'
        )


class CryptoFactory(PaymentFactory):
    def create_button(self) -> PaymentButton:
        return CryptoButton()

    def create_form(self) -> PaymentForm:
        return CryptoForm()

    def get_name(self) -> str:
        return "Криптовалюта"

    def get_icon(self) -> str:
        return "₿"


# ── Реестр фабрик ────────────────────────────

PAYMENT_FACTORIES: dict[str, PaymentFactory] = {
    "paypal": PayPalFactory(),
    "card": BankCardFactory(),
    "crypto": CryptoFactory(),
}


def get_payment_factory(method: str) -> PaymentFactory:
    factory = PAYMENT_FACTORIES.get(method)
    if factory is None:
        raise ValueError(f"Неизвестный способ оплаты: {method}")
    return factory
