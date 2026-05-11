from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self):
        self.successor: "Handler | None" = None
    
    def set_successor(self, successor: "Handler") -> "Handler":
        self.successor = successor
        return successor
    
    @abstractmethod
    def handle_request(self, request: dict) -> dict:
        ...


class StockValidationHandler(Handler):
    def handle_request(self, request: dict) -> dict:
        order_items = request.get("items", [])
        for item in order_items:
            stock = item.get("quantity", 0)
            if stock <= 0:
                return {
                    "status": "rejected",
                    "error": f"Товар {item.get('product_id')} отсутствует на складе",
                    "handler": "StockValidationHandler"
                }
        
        request["stock_validated"] = True
        
        # Передаем запрос преемнику
        if self.successor:
            return self.successor.handle_request(request)
        
        return {"status": "approved", "handler": "StockValidationHandler"}


class PaymentValidationHandler(Handler):
    VALID_METHODS = ["card", "paypal", "crypto", "bank_transfer"]
    
    def handle_request(self, request: dict) -> dict:
        payment_method = request.get("payment_method", "").strip().lower()
        
        if payment_method not in self.VALID_METHODS:
            return {
                "status": "rejected",
                "error": f"Способ оплаты '{payment_method}' не поддерживается",
                "handler": "PaymentValidationHandler",
                "valid_methods": self.VALID_METHODS
            }
        
        request["payment_validated"] = True
        
        # Передаем запрос преемнику
        if self.successor:
            return self.successor.handle_request(request)
        
        return {"status": "approved", "handler": "PaymentValidationHandler"}


class DeliveryValidationHandler(Handler):
    VALID_METHODS = ["courier", "pickup", "express", "post"]
    
    def handle_request(self, request: dict) -> dict:
        delivery_method = request.get("delivery_method", "").strip().lower()
        
        if delivery_method not in self.VALID_METHODS:
            return {
                "status": "rejected",
                "error": f"Способ доставки '{delivery_method}' недоступен",
                "handler": "DeliveryValidationHandler",
                "valid_methods": self.VALID_METHODS
            }
        
        request["delivery_validated"] = True
        
        # Передаем запрос преемнику
        if self.successor:
            return self.successor.handle_request(request)
        
        return {"status": "approved", "handler": "DeliveryValidationHandler"}


class PromoCodeValidationHandler(Handler):
    VALID_PROMO_CODES = {
        "SAVE10": 0.10,
        "SAVE20": 0.20,
        "SAVE50": 0.50,
        "NEWYEAR": 0.15,
        "VIP30": 0.30,
    }
    
    def handle_request(self, request: dict) -> dict:
        promo_code = request.get("promo_code", "").strip().upper()
        
        if promo_code:
            if promo_code not in self.VALID_PROMO_CODES:
                return {
                    "status": "rejected",
                    "error": f"Промокод '{promo_code}' не действителен",
                    "handler": "PromoCodeValidationHandler"
                }
            
            discount = self.VALID_PROMO_CODES[promo_code]
            request["discount_percent"] = discount * 100
            request["promo_validated"] = True
        
        # Передаем запрос преемнику
        if self.successor:
            return self.successor.handle_request(request)
        
        return {"status": "approved", "handler": "PromoCodeValidationHandler"}


class FraudDetectionHandler(Handler):
    def handle_request(self, request: dict) -> dict:
        total = request.get("total", 0)
        
        # Проверяем сумму
        if total > 100000:
            return {
                "status": "suspicious",
                "error": "Заказ требует дополнительной проверки (высокая сумма)",
                "handler": "FraudDetectionHandler",
                "total": total
            }
        
        request["fraud_checked"] = True
        
        # Передаем запрос преемнику
        if self.successor:
            return self.successor.handle_request(request)
        
        return {"status": "approved", "handler": "FraudDetectionHandler"}


class OrderProcessingClient:
    def __init__(self):
        self.chain: Handler | None = None
    
    def set_chain(self, handler: Handler):
        self.chain = handler
    
    def process_order(self, order_data: dict) -> dict:
        if not self.chain:
            return {"error": "Цепочка обработчиков не инициализирована"}
        return self.chain.handle_request(order_data)


def create_order_processing_chain() -> Handler:
    handler1 = StockValidationHandler()
    handler2 = PaymentValidationHandler()
    handler3 = DeliveryValidationHandler()
    handler4 = PromoCodeValidationHandler()
    handler5 = FraudDetectionHandler()
    
    handler1.set_successor(handler2) \
            .set_successor(handler3) \
            .set_successor(handler4) \
            .set_successor(handler5)
    
    return handler1


def process_order_request(order_data: dict) -> dict:
    client = OrderProcessingClient()
    chain = create_order_processing_chain()
    client.set_chain(chain)
    return client.process_order(order_data)
