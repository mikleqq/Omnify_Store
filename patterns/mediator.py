from abc import ABC, abstractmethod
from typing import Any, dict as DictType
from datetime import datetime

class Colleague(ABC):
    
    def __init__(self, name: str, mediator: "Mediator" = None):
        self.name = name
        self.mediator = mediator
    
    @abstractmethod
    def changed(self):
        ...
    
    def set_mediator(self, mediator: "Mediator"):
        self.mediator = mediator

class UserColleague(Colleague):

    
    def __init__(self, name: str, user_id: str, mediator: "Mediator" = None):
        super().__init__(name, mediator)
        self.user_id = user_id
        self.status = "idle"
    
    def changed(self):
    
        if self.mediator:
            self.mediator.colleague_changed(self)
    
    def set_status(self, status: str):
    
        self.status = status
        self.changed()
    
    def get_info(self) -> dict:
    
        return {
            "user_id": self.user_id,
            "name": self.name,
            "status": self.status
        }

class OrderColleague(Colleague):

    
    def __init__(self, name: str, order_id: str, mediator: "Mediator" = None):
        super().__init__(name, mediator)
        self.order_id = order_id
        self.status = "created"
        self.amount = 0.0
    
    def changed(self):
    
        if self.mediator:
            self.mediator.colleague_changed(self)
    
    def set_status(self, status: str):
    
        self.status = status
        self.changed()
    
    def set_amount(self, amount: float):
    
        self.amount = amount
        self.changed()
    
    def get_info(self) -> dict:
    
        return {
            "order_id": self.order_id,
            "name": self.name,
            "status": self.status,
            "amount": self.amount
        }

class NotificationColleague(Colleague):

    
    def __init__(self, name: str, mediator: "Mediator" = None):
        super().__init__(name, mediator)
        self.notifications_sent = []
    
    def changed(self):
    
        if self.mediator:
            self.mediator.colleague_changed(self)
    
    def send_notification(self, event: str, data: dict):
    
        notification = {
            "event": event,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.notifications_sent.append(notification)
        self.changed()
    
    def get_info(self) -> dict:
    
        return {
            "service": self.name,
            "notifications_count": len(self.notifications_sent),
            "last_notifications": self.notifications_sent[-3:]
        }

class PaymentColleague(Colleague):

    
    def __init__(self, name: str, mediator: "Mediator" = None):
        super().__init__(name, mediator)
        self.status = "idle"
        self.last_transaction = None
    
    def changed(self):
    
        if self.mediator:
            self.mediator.colleague_changed(self)
    
    def process_payment(self, amount: float, method: str):
    
        self.last_transaction = {
            "amount": amount,
            "method": method,
            "status": "processed",
            "timestamp": datetime.now().isoformat()
        }
        self.status = "processed"
        self.changed()
    
    def get_info(self) -> dict:
    
        return {
            "service": self.name,
            "status": self.status,
            "last_transaction": self.last_transaction
        }

class InventoryColleague(Colleague):

    
    def __init__(self, name: str, mediator: "Mediator" = None):
        super().__init__(name, mediator)
        self.status = "idle"
        self.items = {}
    
    def changed(self):
    
        if self.mediator:
            self.mediator.colleague_changed(self)
    
    def reserve_items(self, items: dict) -> bool:
    
        self.status = "reserving"
        self.items = items
        self.changed()
        return True
    
    def get_info(self) -> dict:
    
        return {
            "service": self.name,
            "status": self.status,
            "items": self.items
        }

class Mediator(ABC):

    
    @abstractmethod
    def colleague_changed(self, colleague: Colleague):
    
        ...

class OrderProcessingMediator(Mediator):

    
    def __init__(self, name: str = "OrderProcessingMediator"):
        self.name = name
        self.colleagues: dict[str, Colleague] = {}
        self.event_log: list[dict] = []
    
    def register_colleague(self, key: str, colleague: Colleague):
    
        colleague.set_mediator(self)
        self.colleagues[key] = colleague
    
    def get_colleague(self, key: str) -> Colleague:
    
        return self.colleagues.get(key)
    
    def colleague_changed(self, colleague: Colleague):
    
        event = {
            "colleague": colleague.name,
            "timestamp": datetime.now().isoformat(),
            "colleague_info": colleague.get_info() if hasattr(colleague, 'get_info') else {}
        }
        self.event_log.append(event)
        
        self._handle_colleague_change(colleague)
    
    def _handle_colleague_change(self, colleague: Colleague):
    
        
        if isinstance(colleague, UserColleague):
            if colleague.status == "idle":
                self._notify_order_processing()
        
        elif isinstance(colleague, OrderColleague):
            if colleague.status == "created":
                self._notify_inventory_to_reserve()
            elif colleague.status == "ready_to_pay":
                self._notify_payment_gateway()
            elif colleague.status == "paid":
                self._notify_shipment()
        
        elif isinstance(colleague, PaymentColleague):
            if colleague.status == "processed":
                order = self.get_colleague("order")
                if order:
                    order.set_status("paid")
        
        elif isinstance(colleague, InventoryColleague):
            if colleague.status == "reserving":
                order = self.get_colleague("order")
                if order:
                    order.set_status("ready_to_pay")
        
        elif isinstance(colleague, NotificationColleague):
            pass  # Просто логируем
    
    def _notify_order_processing(self):
    
        notification_service = self.get_colleague("notification")
        if notification_service:
            notification_service.send_notification(
                "order_processing_started",
                {"message": "Начало обработки заказа"}
            )
    
    def _notify_inventory_to_reserve(self):
    
        inventory = self.get_colleague("inventory")
        if inventory:
            inventory.reserve_items({"items": ["item1", "item2"]})
    
    def _notify_payment_gateway(self):
    
        payment = self.get_colleague("payment")
        if payment:
            payment.process_payment(1000.0, "card")
    
    def _notify_shipment(self):
    
        notification_service = self.get_colleague("notification")
        if notification_service:
            notification_service.send_notification(
                "order_shipped",
                {"message": "Заказ отправлен"}
            )
    
    def process_order(self, user_id: str, order_id: str) -> dict:
    
        order = self.get_colleague("order")
        if order and isinstance(order, OrderColleague):
            order.order_id = order_id
            order.set_status("created")
            order.set_amount(1000.0)
        
        return {
            "success": True,
            "message": f"Заказ {order_id} обрабатывается",
            "events": self.event_log[-5:]  # Последние 5 событий
        }
    
    def get_statistics(self) -> dict:
    
        return {
            "mediator_name": self.name,
            "colleagues_count": len(self.colleagues),
            "colleagues": list(self.colleagues.keys()),
            "total_events": len(self.event_log)
        }
    
    def get_event_log(self) -> list[dict]:
    
        return self.event_log

def create_order_processing_system() -> tuple[OrderProcessingMediator, dict]:

    
    mediator = OrderProcessingMediator("OrderSystem")
    
    user = UserColleague("User Manager", "user1")
    order = OrderColleague("Order Manager", "order1")
    notification = NotificationColleague("Notification Service")
    payment = PaymentColleague("Payment Gateway")
    inventory = InventoryColleague("Inventory Manager")
    
    mediator.register_colleague("user", user)
    mediator.register_colleague("order", order)
    mediator.register_colleague("notification", notification)
    mediator.register_colleague("payment", payment)
    mediator.register_colleague("inventory", inventory)
    
    colleagues = {
        "user": user,
        "order": order,
        "notification": notification,
        "payment": payment,
        "inventory": inventory
    }
    
    return mediator, colleagues
