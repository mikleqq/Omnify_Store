from abc import ABC, abstractmethod

class Shape(ABC):

    @abstractmethod
    def bounding_box(self) -> dict:

        ...

    @abstractmethod
    def create_manipulator(self) -> "Manipulator":

        ...

class Line(Shape):

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def bounding_box(self) -> dict:

        return {
            "x": min(self.x1, self.x2),
            "y": min(self.y1, self.y2),
            "width": abs(self.x2 - self.x1),
            "height": abs(self.y2 - self.y1),
        }

    def create_manipulator(self) -> "Manipulator":

        return LineManipulator(self)

class TextView:

    def __init__(self, text: str):
        self.text = text
        self._origin_x = 0
        self._origin_y = 0
        self._width = len(text) * 8  # примерно 8 пикселей на символ
        self._height = 16

    def get_extent(self) -> dict:

        return {
            "origin_x": self._origin_x,
            "origin_y": self._origin_y,
            "width": self._width,
            "height": self._height,
        }

    def set_origin(self, x: int, y: int) -> None:
        self._origin_x = x
        self._origin_y = y

    def get_text(self) -> str:
        return self.text

class TextShape(Shape):

    def __init__(self, text_view: TextView):
        self._text_view = text_view

    def bounding_box(self) -> dict:

        extent = self._text_view.get_extent()
        return {
            "x": extent["origin_x"],
            "y": extent["origin_y"],
            "width": extent["width"],
            "height": extent["height"],
        }

    def create_manipulator(self) -> "Manipulator":

        return TextManipulator(self._text_view)

class Manipulator(ABC):

    @abstractmethod
    def handle_mouse_down(self, x: int, y: int) -> None:

        ...

    @abstractmethod
    def handle_mouse_drag(self, x: int, y: int) -> None:

        ...

    @abstractmethod
    def handle_mouse_up(self, x: int, y: int) -> None:

        ...

    @abstractmethod
    def get_info(self) -> dict:

        ...

class LineManipulator(Manipulator):

    def __init__(self, line: Line):
        self.line = line
        self.dragging = False

    def handle_mouse_down(self, x: int, y: int) -> None:
        self.dragging = True
        print(f"📍 LineManipulator: начало перетаскивания в ({x}, {y})")

    def handle_mouse_drag(self, x: int, y: int) -> None:
        if self.dragging:
            self.line.x2 = x
            self.line.y2 = y

    def handle_mouse_up(self, x: int, y: int) -> None:
        self.dragging = False
        print(f"📍 LineManipulator: конец перетаскивания в ({x}, {y})")

    def get_info(self) -> dict:
        return {
            "type": "Line",
            "x1": self.line.x1,
            "y1": self.line.y1,
            "x2": self.line.x2,
            "y2": self.line.y2,
        }

class TextManipulator(Manipulator):

    def __init__(self, text_view: TextView):
        self.text_view = text_view
        self.dragging = False

    def handle_mouse_down(self, x: int, y: int) -> None:
        self.dragging = True
        self.text_view.set_origin(x, y)
        print(f"📝 TextManipulator: начало редактирования в ({x}, {y})")

    def handle_mouse_drag(self, x: int, y: int) -> None:
        if self.dragging:
            self.text_view.set_origin(x, y)

    def handle_mouse_up(self, x: int, y: int) -> None:
        self.dragging = False
        print(f"📝 TextManipulator: конец редактирования в ({x}, {y})")

    def get_info(self) -> dict:
        extent = self.text_view.get_extent()
        return {
            "type": "TextShape",
            "text": self.text_view.get_text(),
            "x": extent["origin_x"],
            "y": extent["origin_y"],
            "width": extent["width"],
            "height": extent["height"],
        }

class DrawingEditor:

    def __init__(self):
        self.shapes: list[Shape] = []

    def add_shape(self, shape: Shape) -> None:

        self.shapes.append(shape)

    def set_selected_shape(self, shape: Shape) -> Manipulator:

        return shape.create_manipulator()

    def get_all_bounds(self) -> list[dict]:

        return [shape.bounding_box() for shape in self.shapes]

    def get_shape_info(self) -> list[dict]:

        info = []
        for shape in self.shapes:
            manipulator = shape.create_manipulator()
            info.append(manipulator.get_info())
        return info

class PaymentProcessor(ABC):

    @abstractmethod
    def process_payment(self, amount: float, details: dict) -> dict: ...

    @abstractmethod
    def refund(self, transaction_id: str) -> dict: ...

    @abstractmethod
    def get_provider_name(self) -> str: ...

class StripeAPILegacy:

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

    def init_payment(self, value: float, description: str) -> dict:
        return {
            "payment_id": f"YK-{abs(hash(description)) % 100000}",
            "amount": {"value": value, "currency": "RUB"},
            "status": "waiting_for_capture",
            "provider": "ЮKassa",
        }

    def capture_payment(self, payment_id: str) -> dict:
        return {"payment_id": payment_id, "status": "succeeded"}

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
        return {"success": True, "transaction_id": transaction_id}

    def get_provider_name(self) -> str:
        return "ЮKassa"

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

