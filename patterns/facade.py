from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

class Inventory:

    def __init__(self):
        self.stock = {
            "laptop": 5,
            "phone": 10,
            "tablet": 3,
        }

    def check_availability(self, product_id: str, quantity: int) -> bool:

        available = self.stock.get(product_id, 0)
        print(f"🏦 Inventory: Проверка {product_id} x{quantity} (в наличии: {available})")
        return available >= quantity

    def reserve_items(self, product_id: str, quantity: int) -> bool:

        if self.check_availability(product_id, quantity):
            self.stock[product_id] -= quantity
            print(f"🏦 Inventory: Зарезервировано {product_id} x{quantity}")
            return True
        print(f"🏦 Inventory: Не удалось зарезервировать {product_id} x{quantity}")
        return False

    def release_items(self, product_id: str, quantity: int) -> None:

        self.stock[product_id] += quantity
        print(f"🏦 Inventory: Освобождено {product_id} x{quantity}")

class PaymentGateway:

    def authorize_payment(self, amount: float, payment_method: str) -> bool:

        print(f"💳 Payment: Авторизация {amount}₽ через {payment_method}")
        success = amount > 0 and payment_method in ["card", "paypal", "crypto"]
        if success:
            print(f"💳 Payment: Авторизация успешна")
        else:
            print(f"💳 Payment: Авторизация не удалась")
        return success

    def capture_payment(self, amount: float) -> str:

        print(f"💳 Payment: Захват платежа {amount}₽")
        transaction_id = f"TXN-{abs(hash(amount)) % 100000}"
        print(f"💳 Payment: Платёж захвачен. ID: {transaction_id}")
        return transaction_id

    def refund_payment(self, transaction_id: str, amount: float) -> bool:

        print(f"💳 Payment: Возврат {amount}₽ для {transaction_id}")
        print(f"💳 Payment: Возврат обработан")
        return True

class ShippingService:

    def calculate_shipping(self, weight_kg: float, distance_km: float) -> float:

        cost = 2.0 + weight_kg * 0.5 + distance_km * 0.01
        print(f"🚚 Shipping: Расчёт доставки: вес {weight_kg}кг, расстояние {distance_km}км = {cost}₽")
        return cost

    def create_shipment(self, order_id: str, address: str, weight_kg: float) -> str:

        print(f"🚚 Shipping: Создание отправки для {order_id}")
        print(f"🚚 Shipping: Адрес: {address}, вес: {weight_kg}кг")
        shipment_id = f"SHIP-{abs(hash(order_id)) % 100000}"
        print(f"🚚 Shipping: Отправка создана. ID: {shipment_id}")
        return shipment_id

    def schedule_delivery(self, shipment_id: str) -> str:

        print(f"🚚 Shipping: Планирование доставки для {shipment_id}")
        estimated_date = "2026-04-08"
        print(f"🚚 Shipping: Предполагаемая дата доставки: {estimated_date}")
        return estimated_date

class NotificationService:

    def send_order_confirmation(self, order_id: str, email: str) -> bool:

        print(f"📧 Notification: Подтверждение заказа {order_id} отправлено на {email}")
        return True

    def send_payment_confirmation(self, order_id: str, email: str, amount: float) -> bool:

        print(f"📧 Notification: Подтверждение платежа {amount}₽ на {email}")
        return True

    def send_shipment_notification(self, order_id: str, email: str, shipment_id: str) -> bool:

        print(f"📧 Notification: Уведомление об отправке {shipment_id} на {email}")
        return True

    def send_delivery_notification(self, order_id: str, email: str, delivery_date: str) -> bool:

        print(f"📧 Notification: Уведомление о доставке {delivery_date} на {email}")
        return True

class OrderValidation:

    def validate_order_items(self, items: List[dict]) -> bool:

        print(f"✅ Validation: Проверка {len(items)} товаров...")
        for item in items:
            if "product_id" not in item or "quantity" not in item:
                print(f"✅ Validation: Ошибка в товаре: {item}")
                return False
        print(f"✅ Validation: Все товары валидны")
        return True

    def validate_customer_info(self, customer_email: str, address: str) -> bool:

        print(f"✅ Validation: Проверка email {customer_email} и адреса...")
        if not customer_email or not address:
            print(f"✅ Validation: Email или адрес отсутствуют")
            return False
        print(f"✅ Validation: Информация клиента валидна")
        return True

    def validate_payment_method(self, payment_method: str) -> bool:

        print(f"✅ Validation: Проверка способа оплаты {payment_method}...")
        valid_methods = ["card", "paypal", "crypto"]
        is_valid = payment_method in valid_methods
        if is_valid:
            print(f"✅ Validation: Способ оплаты валиден")
        else:
            print(f"✅ Validation: Неподдерживаемый способ оплаты")
        return is_valid

class OrderProcessingFacade:

    def __init__(self):
        self.inventory = Inventory()
        self.payment = PaymentGateway()
        self.shipping = ShippingService()
        self.notification = NotificationService()
        self.validation = OrderValidation()

    def process_order(
        self,
        order_id: str,
        items: List[dict],
        customer_email: str,
        address: str,
        payment_method: str,
        total_amount: float
    ) -> dict:

        
        print("=" * 80)
        print(f"🎯 ФАСАД: Начало обработки заказа {order_id}")
        print("=" * 80)
        
        print("\n[ШАГ 1] Валидация...")
        if not self.validation.validate_order_items(items):
            return {"success": False, "error": "Invalid items"}
        
        if not self.validation.validate_customer_info(customer_email, address):
            return {"success": False, "error": "Invalid customer info"}
        
        if not self.validation.validate_payment_method(payment_method):
            return {"success": False, "error": "Invalid payment method"}
        
        print("\n[ШАГ 2] Проверка наличия товаров...")
        for item in items:
            if not self.inventory.reserve_items(item["product_id"], item["quantity"]):
                for prev_item in items:
                    if prev_item == item:
                        break
                    self.inventory.release_items(prev_item["product_id"], prev_item["quantity"])
                return {"success": False, "error": "Not enough inventory"}
        
        print("\n[ШАГ 3] Обработка платежа...")
        if not self.payment.authorize_payment(total_amount, payment_method):
            for item in items:
                self.inventory.release_items(item["product_id"], item["quantity"])
            return {"success": False, "error": "Payment authorization failed"}
        
        transaction_id = self.payment.capture_payment(total_amount)
        
        print("\n[ШАГ 4] Организация доставки...")
        weight_kg = len(items) * 0.5
        distance_km = 15  # ~средний расстояние
        shipping_cost = self.shipping.calculate_shipping(weight_kg, distance_km)
        
        shipment_id = self.shipping.create_shipment(order_id, address, weight_kg)
        delivery_date = self.shipping.schedule_delivery(shipment_id)
        
        print("\n[ШАГ 5] Отправка уведомлений...")
        self.notification.send_order_confirmation(order_id, customer_email)
        self.notification.send_payment_confirmation(order_id, customer_email, total_amount)
        self.notification.send_shipment_notification(order_id, customer_email, shipment_id)
        self.notification.send_delivery_notification(order_id, customer_email, delivery_date)
        
        print("\n" + "=" * 80)
        print(f"✅ ФАСАД: Заказ {order_id} успешно обработан!")
        print("=" * 80)
        
        return {
            "success": True,
            "order_id": order_id,
            "transaction_id": transaction_id,
            "shipment_id": shipment_id,
            "delivery_date": delivery_date,
            "shipping_cost": shipping_cost,
            "total_amount": total_amount + shipping_cost,
        }

    def cancel_order(self, order_id: str, items: List[dict], transaction_id: str, amount: float) -> bool:

        
        print("\n" + "=" * 80)
        print(f"🔄 ФАСАД: Отмена заказа {order_id}")
        print("=" * 80)
        
        print("\n[ОТМЕНА] Освобождение товаров...")
        for item in items:
            self.inventory.release_items(item["product_id"], item["quantity"])
        
        print("[ОТМЕНА] Возврат платежа...")
        self.payment.refund_payment(transaction_id, amount)
        
        print("\n✅ Заказ отменён!")
        return True
