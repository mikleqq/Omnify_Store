from abc import ABC, abstractmethod
from typing import Callable




class NotificationObserver(ABC):
    @abstractmethod
    def update(self, event: str, data: dict) -> str:

        ...

    @abstractmethod
    def get_channel(self) -> str: ...


class EmailObserver(NotificationObserver):
    def __init__(self, email: str):
        self.email = email

    def get_channel(self) -> str:
        return "Email"

    def update(self, event: str, data: dict) -> str:
        messages = {
            "order_placed": f"✉️ Email → {self.email}: Заказ #{data.get('order_id')} оформлен! Сумма: {data.get('total')} ₽",
            "order_paid": f"✉️ Email → {self.email}: Оплата заказа #{data.get('order_id')} подтверждена.",
            "order_shipped": f"✉️ Email → {self.email}: Заказ #{data.get('order_id')} передан в доставку.",
            "order_delivered": f"✉️ Email → {self.email}: Заказ #{data.get('order_id')} доставлен. Спасибо!",
        }
        return messages.get(event, f"✉️ Email → {self.email}: Событие «{event}» для заказа #{data.get('order_id')}")


class SMSObserver(NotificationObserver):
    def __init__(self, phone: str):
        self.phone = phone

    def get_channel(self) -> str:
        return "SMS"

    def update(self, event: str, data: dict) -> str:
        messages = {
            "order_placed": f"📱 SMS → {self.phone}: Заказ #{data.get('order_id')} принят. Сумма: {data.get('total')} ₽",
            "order_paid": f"📱 SMS → {self.phone}: Оплата #{data.get('order_id')} прошла успешно.",
            "order_shipped": f"📱 SMS → {self.phone}: Заказ #{data.get('order_id')} в пути!",
            "order_delivered": f"📱 SMS → {self.phone}: Заказ #{data.get('order_id')} доставлен.",
        }
        return messages.get(event, f"📱 SMS → {self.phone}: Событие «{event}» для заказа #{data.get('order_id')}")


class PushObserver(NotificationObserver):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_channel(self) -> str:
        return "Push"

    def update(self, event: str, data: dict) -> str:
        return f"🔔 Push → пользователь {self.user_id}: [{event.upper()}] Заказ #{data.get('order_id')}"


class NotificationService:


    def __init__(self):
        self._observers: list[NotificationObserver] = []
        self.log: list[str] = []

    def subscribe(self, observer: NotificationObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: NotificationObserver) -> None:
        self._observers.remove(observer)

    def notify(self, event: str, data: dict) -> list[str]:
        messages = []
        for obs in self._observers:
            msg = obs.update(event, data)
            self.log.append(msg)
            messages.append(msg)
        return messages

    def clear(self) -> None:
        self._observers.clear()



notification_service = NotificationService()
