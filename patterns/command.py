# ─────────────────────────────────────────────
#  COMMAND  –  команды операций
# ─────────────────────────────────────────────
#
#  Структура:
#  - Command (базовый интерфейс команды)
#  - ConcreteCommand (конкретная команда с ссылкой на Receiver)
#  - Receiver (объект, который выполняет операцию)
#  - Invoker (инициатор команды)
#  - Client (клиент, создает команды и назначает им получателей)
#

from abc import ABC, abstractmethod
from datetime import datetime


# ── COMMAND ──────────────────────────────────

class Command(ABC):
    """
    Абстрактная команда (Command)
    Определяет интерфейс для выполнения операции
    """
    
    @abstractmethod
    def execute(self) -> dict:
        """Выполняет команду"""
        ...


# ── RECEIVER ─────────────────────────────────

class OrderReceiver:
    """
    Receiver - объект, который выполняет операцию
    Содержит бизнес-логику действий с заказом
    """
    
    def __init__(self, order_id: str, user_id: str):
        self.order_id = order_id
        self.user_id = user_id
        self.status = "created"
        self.created_at = datetime.now().isoformat()
    
    def place_order(self) -> dict:
        """Action() - размещает заказ"""
        self.status = "placed"
        return {
            "order_id": self.order_id,
            "status": "placed",
            "message": f"Заказ #{self.order_id} размещен"
        }
    
    def pay_order(self, amount: float, payment_method: str) -> dict:
        """Action() - оплачивает заказ"""
        self.status = "paid"
        return {
            "order_id": self.order_id,
            "status": "paid",
            "amount": amount,
            "payment_method": payment_method,
            "message": f"Заказ #{self.order_id} оплачен на сумму {amount} ₽"
        }
    
    def cancel_order(self, reason: str = "") -> dict:
        """Action() - отменяет заказ"""
        self.status = "cancelled"
        return {
            "order_id": self.order_id,
            "status": "cancelled",
            "reason": reason,
            "message": f"Заказ #{self.order_id} отменен"
        }
    
    def ship_order(self, tracking_number: str) -> dict:
        """Action() - отправляет заказ"""
        self.status = "shipped"
        return {
            "order_id": self.order_id,
            "status": "shipped",
            "tracking_number": tracking_number,
            "message": f"Заказ #{self.order_id} отправлен. Трек: {tracking_number}"
        }
    
    def deliver_order(self) -> dict:
        """Action() - доставляет заказ"""
        self.status = "delivered"
        return {
            "order_id": self.order_id,
            "status": "delivered",
            "message": f"Заказ #{self.order_id} доставлен"
        }
    
    def refund_order(self, amount: float, reason: str = "") -> dict:
        """Action() - возвращает деньги"""
        self.status = "refunded"
        return {
            "order_id": self.order_id,
            "status": "refunded",
            "amount": amount,
            "reason": reason,
            "message": f"Заказ #{self.order_id}: возврат {amount} ₽"
        }


# ── CONCRETE COMMANDS ────────────────────────

class PlaceOrderCommand(Command):
    """ConcreteCommand - Команда размещения заказа"""
    
    def __init__(self, receiver: OrderReceiver):
        self.receiver = receiver
        self.executed_at = None
    
    def execute(self) -> dict:
        """Execute() - вызывает Action() объекта Receiver"""
        self.executed_at = datetime.now().isoformat()
        result = self.receiver.place_order()
        return {
            **result,
            "command": "PlaceOrderCommand",
            "executed_at": self.executed_at
        }


class PayOrderCommand(Command):
    """ConcreteCommand - Команда оплаты заказа"""
    
    def __init__(self, receiver: OrderReceiver, amount: float, payment_method: str):
        self.receiver = receiver
        self.amount = amount
        self.payment_method = payment_method
        self.executed_at = None
    
    def execute(self) -> dict:
        """Execute() - вызывает Action() объекта Receiver"""
        self.executed_at = datetime.now().isoformat()
        result = self.receiver.pay_order(self.amount, self.payment_method)
        return {
            **result,
            "command": "PayOrderCommand",
            "executed_at": self.executed_at
        }


class CancelOrderCommand(Command):
    """ConcreteCommand - Команда отмены заказа"""
    
    def __init__(self, receiver: OrderReceiver, reason: str = ""):
        self.receiver = receiver
        self.reason = reason
        self.executed_at = None
    
    def execute(self) -> dict:
        """Execute() - вызывает Action() объекта Receiver"""
        self.executed_at = datetime.now().isoformat()
        result = self.receiver.cancel_order(self.reason)
        return {
            **result,
            "command": "CancelOrderCommand",
            "executed_at": self.executed_at
        }


class ShipOrderCommand(Command):
    """ConcreteCommand - Команда отправки заказа"""
    
    def __init__(self, receiver: OrderReceiver, tracking_number: str):
        self.receiver = receiver
        self.tracking_number = tracking_number
        self.executed_at = None
    
    def execute(self) -> dict:
        """Execute() - вызывает Action() объекта Receiver"""
        self.executed_at = datetime.now().isoformat()
        result = self.receiver.ship_order(self.tracking_number)
        return {
            **result,
            "command": "ShipOrderCommand",
            "executed_at": self.executed_at
        }


class DeliverOrderCommand(Command):
    """ConcreteCommand - Команда доставки заказа"""
    
    def __init__(self, receiver: OrderReceiver):
        self.receiver = receiver
        self.executed_at = None
    
    def execute(self) -> dict:
        """Execute() - вызывает Action() объекта Receiver"""
        self.executed_at = datetime.now().isoformat()
        result = self.receiver.deliver_order()
        return {
            **result,
            "command": "DeliverOrderCommand",
            "executed_at": self.executed_at
        }


class RefundOrderCommand(Command):
    """ConcreteCommand - Команда возврата заказа"""
    
    def __init__(self, receiver: OrderReceiver, amount: float, reason: str = ""):
        self.receiver = receiver
        self.amount = amount
        self.reason = reason
        self.executed_at = None
    
    def execute(self) -> dict:
        """Execute() - вызывает Action() объекта Receiver"""
        self.executed_at = datetime.now().isoformat()
        result = self.receiver.refund_order(self.amount, self.reason)
        return {
            **result,
            "command": "RefundOrderCommand",
            "executed_at": self.executed_at
        }


# ── INVOKER ──────────────────────────────────

class OrderInvoker:
    """
    Invoker (MenuItem) - Инициатор команды
    Содержит команду и вызывает ее execute()
    """
    
    def __init__(self, name: str = "OrderInvoker"):
        self.name = name
        self.command: Command | None = None
        self.history: list[dict] = []
    
    def set_command(self, command: Command):
        """Устанавливает команду для выполнения"""
        self.command = command
    
    def execute_command(self) -> dict:
        """Выполняет установленную команду"""
        if not self.command:
            return {"error": "Команда не установлена"}
        
        result = self.command.execute()
        self.history.append(result)
        return result
    
    def get_history(self) -> list[dict]:
        """Возвращает историю выполненных команд"""
        return self.history


# ── CLIENT ───────────────────────────────────

class OrderManagementClient:
    """
    Client (Application) - Клиент
    Создает ConcreteCommand и устанавливает получателя (Receiver)
    """
    
    def __init__(self):
        self.invoker = OrderInvoker("OrderSystem")
    
    def request_place_order(self, order_id: str, user_id: str) -> dict:
        """Клиент создает команду и выполняет ее"""
        receiver = OrderReceiver(order_id, user_id)
        command = PlaceOrderCommand(receiver)
        self.invoker.set_command(command)
        return self.invoker.execute_command()
    
    def request_pay_order(self, order_id: str, user_id: str, amount: float, payment_method: str) -> dict:
        """Клиент создает команду оплаты"""
        receiver = OrderReceiver(order_id, user_id)
        command = PayOrderCommand(receiver, amount, payment_method)
        self.invoker.set_command(command)
        return self.invoker.execute_command()
    
    def request_cancel_order(self, order_id: str, user_id: str, reason: str = "") -> dict:
        """Клиент создает команду отмены"""
        receiver = OrderReceiver(order_id, user_id)
        command = CancelOrderCommand(receiver, reason)
        self.invoker.set_command(command)
        return self.invoker.execute_command()
    
    def request_ship_order(self, order_id: str, user_id: str, tracking_number: str) -> dict:
        """Клиент создает команду отправки"""
        receiver = OrderReceiver(order_id, user_id)
        command = ShipOrderCommand(receiver, tracking_number)
        self.invoker.set_command(command)
        return self.invoker.execute_command()
    
    def request_deliver_order(self, order_id: str, user_id: str) -> dict:
        """Клиент создает команду доставки"""
        receiver = OrderReceiver(order_id, user_id)
        command = DeliverOrderCommand(receiver)
        self.invoker.set_command(command)
        return self.invoker.execute_command()
    
    def request_refund_order(self, order_id: str, user_id: str, amount: float, reason: str = "") -> dict:
        """Клиент создает команду возврата"""
        receiver = OrderReceiver(order_id, user_id)
        command = RefundOrderCommand(receiver, amount, reason)
        self.invoker.set_command(command)
        return self.invoker.execute_command()
    
    def get_command_history(self) -> list[dict]:
        """Получает историю команд"""
        return self.invoker.get_history()
