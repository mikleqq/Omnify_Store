# ─────────────────────────────────────────────
#  MEDIATOR  –  посредник между объектами
# ─────────────────────────────────────────────
#
#  Структура:
#  - Mediator (DialogDirector) - интерфейс для обмена информацией
#  - ConcreteMediator - конкретный посредник, управляет объектами Colleague
#  - Colleague (ListBox, EntryField) - коллега, знает о посреднике
#  - ConcreteColleague1, ConcreteColleague2 - конкретные коллеги
#  - Все коллеги общаются только через посредника
#

from abc import ABC, abstractmethod
from typing import Any, dict as DictType
from datetime import datetime


# ── COLLEAGUE ────────────────────────────────

class Colleague(ABC):
    """
    Colleague (ListBox, EntryField)
    Абстрактный коллега - знает о своем посреднике и общается только через него
    """
    
    def __init__(self, name: str, mediator: "Mediator" = None):
        self.name = name
        self.mediator = mediator
    
    @abstractmethod
    def changed(self):
        """Changed() - оповещает посредника об изменении"""
        ...
    
    def set_mediator(self, mediator: "Mediator"):
        """Устанавливает посредника"""
        self.mediator = mediator


# ── CONCRETE COLLEAGUES ──────────────────────

class UserColleague(Colleague):
    """
    ConcreteColleague1 - Пользователь
    Знает посредника и отправляет ему уведомления об изменениях
    """
    
    def __init__(self, name: str, user_id: str, mediator: "Mediator" = None):
        super().__init__(name, mediator)
        self.user_id = user_id
        self.status = "idle"
    
    def changed(self):
        """Changed() - уведомляет посредника об изменении"""
        if self.mediator:
            self.mediator.colleague_changed(self)
    
    def set_status(self, status: str):
        """Изменяет статус пользователя"""
        self.status = status
        self.changed()
    
    def get_info(self) -> dict:
        """Возвращает информацию о пользователе"""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "status": self.status
        }


class OrderColleague(Colleague):
    """
    ConcreteColleague2 - Заказ
    Знает посредника и отправляет ему уведомления об изменениях
    """
    
    def __init__(self, name: str, order_id: str, mediator: "Mediator" = None):
        super().__init__(name, mediator)
        self.order_id = order_id
        self.status = "created"
        self.amount = 0.0
    
    def changed(self):
        """Changed() - уведомляет посредника об изменении"""
        if self.mediator:
            self.mediator.colleague_changed(self)
    
    def set_status(self, status: str):
        """Изменяет статус заказа"""
        self.status = status
        self.changed()
    
    def set_amount(self, amount: float):
        """Устанавливает сумму заказа"""
        self.amount = amount
        self.changed()
    
    def get_info(self) -> dict:
        """Возвращает информацию о заказе"""
        return {
            "order_id": self.order_id,
            "name": self.name,
            "status": self.status,
            "amount": self.amount
        }


class NotificationColleague(Colleague):
    """
    ConcreteColleague3 - Сервис уведомлений
    Знает посредника и отправляет ему уведомления об изменениях
    """
    
    def __init__(self, name: str, mediator: "Mediator" = None):
        super().__init__(name, mediator)
        self.notifications_sent = []
    
    def changed(self):
        """Changed() - уведомляет посредника об изменении"""
        if self.mediator:
            self.mediator.colleague_changed(self)
    
    def send_notification(self, event: str, data: dict):
        """Отправляет уведомление"""
        notification = {
            "event": event,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.notifications_sent.append(notification)
        self.changed()
    
    def get_info(self) -> dict:
        """Возвращает информацию об уведомлениях"""
        return {
            "service": self.name,
            "notifications_count": len(self.notifications_sent),
            "last_notifications": self.notifications_sent[-3:]
        }


class PaymentColleague(Colleague):
    """
    ConcreteColleague4 - Платежный шлюз
    Знает посредника и отправляет ему уведомления об изменениях
    """
    
    def __init__(self, name: str, mediator: "Mediator" = None):
        super().__init__(name, mediator)
        self.status = "idle"
        self.last_transaction = None
    
    def changed(self):
        """Changed() - уведомляет посредника об изменении"""
        if self.mediator:
            self.mediator.colleague_changed(self)
    
    def process_payment(self, amount: float, method: str):
        """Обрабатывает платеж"""
        self.last_transaction = {
            "amount": amount,
            "method": method,
            "status": "processed",
            "timestamp": datetime.now().isoformat()
        }
        self.status = "processed"
        self.changed()
    
    def get_info(self) -> dict:
        """Возвращает информацию о платежах"""
        return {
            "service": self.name,
            "status": self.status,
            "last_transaction": self.last_transaction
        }


class InventoryColleague(Colleague):
    """
    ConcreteColleague5 - Управление инвентарем
    Знает посредника и отправляет ему уведомления об изменениях
    """
    
    def __init__(self, name: str, mediator: "Mediator" = None):
        super().__init__(name, mediator)
        self.status = "idle"
        self.items = {}
    
    def changed(self):
        """Changed() - уведомляет посредника об изменении"""
        if self.mediator:
            self.mediator.colleague_changed(self)
    
    def reserve_items(self, items: dict) -> bool:
        """Резервирует товары"""
        self.status = "reserving"
        self.items = items
        self.changed()
        return True
    
    def get_info(self) -> dict:
        """Возвращает информацию об инвентаре"""
        return {
            "service": self.name,
            "status": self.status,
            "items": self.items
        }


# ── MEDIATOR ─────────────────────────────────

class Mediator(ABC):
    """
    Mediator (DialogDirector)
    Абстрактный посредник - определяет интерфейс для обмена информацией между коллегами
    """
    
    @abstractmethod
    def colleague_changed(self, colleague: Colleague):
        """
        ColleagueChanged(colleague)
        Вызывается коллегой при его изменении
        """
        ...


# ── CONCRETE MEDIATOR ────────────────────────

class OrderProcessingMediator(Mediator):
    """
    ConcreteMediator (DialogDirector)
    Конкретный посредник - реализует интерфейс для координации объектов Colleague
    Содержит ссылки на объекты Colleague и управляет их взаимодействием
    """
    
    def __init__(self, name: str = "OrderProcessingMediator"):
        self.name = name
        self.colleagues: dict[str, Colleague] = {}
        self.event_log: list[dict] = []
    
    def register_colleague(self, key: str, colleague: Colleague):
        """Регистрирует коллегу в системе"""
        colleague.set_mediator(self)
        self.colleagues[key] = colleague
    
    def get_colleague(self, key: str) -> Colleague:
        """Получает коллегу по ключу"""
        return self.colleagues.get(key)
    
    def colleague_changed(self, colleague: Colleague):
        """
        ColleagueChanged(colleague)
        Вызывается коллегой при его изменении
        Реализует логику взаимодействия между коллегами
        """
        event = {
            "colleague": colleague.name,
            "timestamp": datetime.now().isoformat(),
            "colleague_info": colleague.get_info() if hasattr(colleague, 'get_info') else {}
        }
        self.event_log.append(event)
        
        # Логика координации между коллегами
        self._handle_colleague_change(colleague)
    
    def _handle_colleague_change(self, colleague: Colleague):
        """Обрабатывает изменение коллеги и координирует действия других"""
        
        # Если изменился пользователь
        if isinstance(colleague, UserColleague):
            if colleague.status == "idle":
                self._notify_order_processing()
        
        # Если изменился заказ
        elif isinstance(colleague, OrderColleague):
            if colleague.status == "created":
                self._notify_inventory_to_reserve()
            elif colleague.status == "ready_to_pay":
                self._notify_payment_gateway()
            elif colleague.status == "paid":
                self._notify_shipment()
        
        # Если платеж обработан
        elif isinstance(colleague, PaymentColleague):
            if colleague.status == "processed":
                order = self.get_colleague("order")
                if order:
                    order.set_status("paid")
        
        # Если инвентарь обновлен
        elif isinstance(colleague, InventoryColleague):
            if colleague.status == "reserving":
                order = self.get_colleague("order")
                if order:
                    order.set_status("ready_to_pay")
        
        # Если уведомление отправлено
        elif isinstance(colleague, NotificationColleague):
            pass  # Просто логируем
    
    def _notify_order_processing(self):
        """Уведомляет о начале обработки заказа"""
        notification_service = self.get_colleague("notification")
        if notification_service:
            notification_service.send_notification(
                "order_processing_started",
                {"message": "Начало обработки заказа"}
            )
    
    def _notify_inventory_to_reserve(self):
        """Просит инвентарь зарезервировать товары"""
        inventory = self.get_colleague("inventory")
        if inventory:
            inventory.reserve_items({"items": ["item1", "item2"]})
    
    def _notify_payment_gateway(self):
        """Просит платежный шлюз обработать платеж"""
        payment = self.get_colleague("payment")
        if payment:
            payment.process_payment(1000.0, "card")
    
    def _notify_shipment(self):
        """Уведомляет об отправке"""
        notification_service = self.get_colleague("notification")
        if notification_service:
            notification_service.send_notification(
                "order_shipped",
                {"message": "Заказ отправлен"}
            )
    
    def process_order(self, user_id: str, order_id: str) -> dict:
        """
        Запускает полный цикл обработки заказа через координацию коллег
        """
        # Создаем/обновляем заказ
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
        """Возвращает статистику взаимодействий"""
        return {
            "mediator_name": self.name,
            "colleagues_count": len(self.colleagues),
            "colleagues": list(self.colleagues.keys()),
            "total_events": len(self.event_log)
        }
    
    def get_event_log(self) -> list[dict]:
        """Возвращает лог всех событий"""
        return self.event_log


# ── FACTORY FUNCTION ─────────────────────────

def create_order_processing_system() -> tuple[OrderProcessingMediator, dict]:
    """
    Создает полную систему управления заказами с посредником
    """
    
    # Создаем посредника
    mediator = OrderProcessingMediator("OrderSystem")
    
    # Создаем коллег (без посредника, они его получат при регистрации)
    user = UserColleague("User Manager", "user1")
    order = OrderColleague("Order Manager", "order1")
    notification = NotificationColleague("Notification Service")
    payment = PaymentColleague("Payment Gateway")
    inventory = InventoryColleague("Inventory Manager")
    
    # Регистрируем коллег в посреднике
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
