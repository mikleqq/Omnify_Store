# 🏛️ Паттерн Facade – Полная Документация

## 📋 Структура (по диаграмме Compiler)

```
              Client
                 │
                 ↓
           ┌──────────────┐
           │   Compiler   │ ← ФАСАД
           │  Compile()   │
           └──────┬───────┘
                  │
        ┌─────────┼─────────┬──────────┐
        │         │         │          │
   Scanner    Parser    ProgramNode   CodeGenerator
    ↓          ↓         Builder       (ABC)
   Token     Symbol    (ProgramNode) ├─ StackMachine
                                      └─ RISC
                                      
Stream (ABC) ← BytecodeStream
    ↑
CodeGenerator → BytecodeStream
```

## 🔑 Ключевые Компоненты

### 1. **Facade (Фасад)** – ГЛАВНЫЙ КЛАСС

```python
class OrderProcessingFacade:
    """Предоставляет простой интерфейс к сложной подсистеме."""
    
    def __init__(self):
        # Инициализируем все подсистемы
        self.inventory = Inventory()
        self.payment = PaymentGateway()
        self.shipping = ShippingService()
        self.notification = NotificationService()
        self.validation = OrderValidation()
    
    def process_order(self, order_id, items, customer_email, ...) -> dict:
        """Единовременной метод для обработки всего заказа.
        
        Скрывает сложность координации 5 подсистем!
        """
        # 1. Валидация
        # 2. Проверка наличия товаров
        # 3. Обработка платежа
        # 4. Организация доставки
        # 5. Отправка уведомлений
        return {"success": True, ...}
```

**Ключевые черты**:
- ✅ Содержит ссылки на все подсистемы
- ✅ Координирует их работу
- ✅ Предоставляет простой интерфейс `process_order()`
- ✅ Скрывает сложность от клиента

---

### 2. **Subsystems (Подсистемы)**

#### **Inventory** – Управление товарами
```python
class Inventory:
    def check_availability(product_id, quantity) -> bool: ...
    def reserve_items(product_id, quantity) -> bool: ...
    def release_items(product_id, quantity) -> None: ...
```

#### **PaymentGateway** – Обработка платежей
```python
class PaymentGateway:
    def authorize_payment(amount, payment_method) -> bool: ...
    def capture_payment(amount) -> str: ...  # возвращает transaction_id
    def refund_payment(transaction_id, amount) -> bool: ...
```

#### **ShippingService** – Управление доставкой
```python
class ShippingService:
    def calculate_shipping(weight_kg, distance_km) -> float: ...
    def create_shipment(order_id, address, weight_kg) -> str: ...
    def schedule_delivery(shipment_id) -> str: ...
```

#### **NotificationService** – Отправка уведомлений
```python
class NotificationService:
    def send_order_confirmation(order_id, email) -> bool: ...
    def send_payment_confirmation(order_id, email, amount) -> bool: ...
    def send_shipment_notification(order_id, email, shipment_id) -> bool: ...
    def send_delivery_notification(order_id, email, delivery_date) -> bool: ...
```

#### **OrderValidation** – Валидация заказа
```python
class OrderValidation:
    def validate_order_items(items) -> bool: ...
    def validate_customer_info(customer_email, address) -> bool: ...
    def validate_payment_method(payment_method) -> bool: ...
```

---

## 🎯 Как Работает Facade

### Без Facade (Плохо ❌)

```python
# Клиент сам должен координировать все подсистемы!
# Это сложно, ошибкоопасно и нарушает инкапсуляцию

inventory = Inventory()
payment = PaymentGateway()
shipping = ShippingService()
notification = NotificationService()
validation = OrderValidation()

# Клиент знает о всех деталях!
if not validation.validate_order_items(items):
    return error

if not inventory.check_availability(items[0]["product_id"], items[0]["quantity"]):
    return error

# ... ещё 20 строк кода для координации ...

if not payment.authorize_payment(amount, method):
    inventory.release_items(...)  # Отмена!
    return error

# Кошмар! Клиент отвечает за правильный порядок вызовов!
```

### С Facade (Хорошо ✅)

```python
# Просто вызовите один метод фасада!
facade = OrderProcessingFacade()

result = facade.process_order(
    order_id="ORD-001",
    items=[{"product_id": "laptop", "quantity": 1}],
    customer_email="user@example.com",
    address="123 Main St",
    payment_method="card",
    total_amount=1000.0
)

# Фасад скрывает всю сложность!
```

---

## 📊 Поток Выполнения: Обработка Заказа

```
Client: facade.process_order(...)
  │
  ↓
Facade.process_order()
  │
  ├─ [1] Validation.validate_*()
  │       └─ Проверяет заказ, товары, способ оплаты
  │
  ├─ [2] Inventory.reserve_items()
  │       └─ Зарезервировать товары
  │       └─ При ошибке: откатить резервирование
  │
  ├─ [3] Payment.authorize_payment()
  │       └─ Авторизовать платёж
  │       └─ Payment.capture_payment()
  │           └─ Завершить платёж
  │       └─ При ошибке: освободить товары
  │
  ├─ [4] Shipping.calculate_shipping()
  │       └─ Shipping.create_shipment()
  │           └─ Shipping.schedule_delivery()
  │               └─ Запланировать доставку
  │
  ├─ [5] Notification.send_*() (четыре разных уведомления)
  │       └─ Подтверждение заказа
  │       └─ Подтверждение платежа
  │       └─ Уведомление об отправке
  │       └─ Уведомление о доставке
  │
  └─ return {success: true, order_id, transaction_id, shipment_id, ...}
```

---

## ✨ Преимущества Facade

| Преимущество | Объяснение |
|---|---|
| **Упрощает интерфейс** | Клиент работает с одним методом вместо координации 5+ подсистем |
| **Слабая связь** | Клиент не знает о деталях подсистем, они могут менять |
| **Инкапсуляция** | Сложность скрыта внутри фасада |
| **Переиспользование** | Один фасад для всех клиентов |
| **Надежность** | Фасад гарантирует правильный порядок операций |
| **Тестируемость** | Тестируем фасад, а подсистемы мокируем |

---

## ❌ Недостатки Facade

| Проблема | Описание |
|---|---|
| **Всемогущий класс** | Фасад может стать слишком большим (God Object) |
| **Сложность отладки** | Трудно отследить что произошло в какой подсистеме |
| **Скрытие ошибок** | Если какая-то подсистема работает неправильно, это может быть не видно |
| **Неправильное использование** | Клиентам всё равно могут нужны "детали" подсистем |

---

## 🔄 Сравнение с Похожими Паттернами

| Паттерн | Назначение | Когда использовать |
|---------|-----------|-------------------|
| **Facade** | Упростить от сложной системы | Много подсистем, нужен простой интерфейс |
| **Decorator** | Динамич. добавление функций | Runtime опции к одному объекту |
| **Adapter** | Адаптировать интерфейс | Несовместимые интерфейсы |
| **Bridge** | Разделить абстракцию и реал. | 2+ измерения варьирования |
| **Composite** | Древовидная структура | Иерархия объектов |

---

## 🎯 Когда Использовать Facade

✅ **Используйте когда:**

1. **Сложная подсистема**
   - Много классов, много зависимостей
   - Трудно использовать без фасада

2. **Нужен простой интерфейс**
   - Типичные операции выполняются в определённом порядке
   - Можно скрыть сложность

3. **Слабая связь нужна**
   - Клиентов не должны менять при изменении подсистемы
   - Фасад как посредник

4. **Разделение слоёв**
   - Отделить слой приложения (App) от слоя логики (Business)
   - Фасад на границе слоёв

❌ **НЕ используйте когда:**

1. **Простая система**
   - Всего 2-3 класса
   - Стоит ли усложнением?

2. **Клиентам нужна гибкость**
   - Клиенты хотят вызывать методы в нестандартном порядке
   - Фасад ограничивает это

3. **Много разных use cases**
   - Невозможно покрыть все нужные возрастают одним методом фасада
   - Нужны разные фасады или отказаться от фасада

---

## 💻 Практический Пример

### Использование в коде:

```python
# Создаём фасад
facade = OrderProcessingFacade()

# Готовим данные заказа
order = {
    "order_id": "ORD-12345",
    "items": [
        {"product_id": "laptop", "quantity": 1},
        {"product_id": "mouse", "quantity": 2},
    ],
    "customer_email": "john@example.com",
    "address": "123 Main Street",
    "payment_method": "card",
    "total_amount": 1050.00,
}

# Обрабатываем заказ ОДНИМ методом!
result = facade.process_order(**order)

if result["success"]:
    print(f"Заказ обработан!")
    print(f"Платёж: {result['transaction_id']}")
    print(f"Доставка: {result['shipment_id']}")
    print(f"Дата доставки: {result['delivery_date']}")
else:
    print(f"Ошибка: {result['error']}")

# При отмене заказа:
if some_condition:
    facade.cancel_order(order["order_id"], order["items"], 
                       result["transaction_id"], order["total_amount"])
```

---

## 🔍 Когда Фасад Спасает Положение

### Сценарий 1: Новый разработчик

```python
# БЕЗ ФАСАДА: Новый разработчик должен понять, как координировать системы
# Вероятность ошибки: ОГРОМНАЯ
inventory = Inventory()
# Оops! Забыл про validation сначала!
inventory.reserve_items(...)  # Может зафейл!
# ...потом платёж...
# ...потом отправка...
# Какого порядка нужно придерживаться?

# С ФАСАДОМ: Просто один вызов!
facade = OrderProcessingFacade()
facade.process_order(...)  # Всё делает в правильном порядке!
```

### Сценарий 2: Изменение подсистемы

```python
# БЕЗ ФАСАДА: Нужно найти все места, где используется подсистема
# Если добавим новый шаг валидации:
# - Нужно обновить ВСЕ клиентские коды

# С ФАСАДОМ: Обновляем только фасад!
# Фасад инкапсулирует сложность
class OrderProcessingFacade:
    def process_order(self, ...):
        # Добавили новый шаг валидации
        self.validation.validate_duplicate_order(order_id)  # Новое!
        # Клиенты не знают об этом, но получают улучшение!
```

---

## 📚 Настоящие Примеры Facade

### 1. **Django ORM**
```python
# Фасад скрывает SQL complexity:
User.objects.filter(email="john@example.com").first()

# На самом деле за кулисами:
# - Query builder
# - SQL compiler
# - Database connection
# - Result parsing
# Но клиент не видит всего этого!
```

### 2. **Requests Library (Python)**
```python
# Фасад скрывает сложность HTTP:
response = requests.get("https://api.example.com/users")

# На самом деле:
# - Socket connection
# - TLS handshake
# - HTTP protocol
# - Response parsing
# Но это всё скрыто!
```

### 3. **Database Transactions**
```python
# Фасад для транзакций:
adapter = DatabaseAdapter()
with adapter.transaction():
    adapter.insert(...)
    adapter.update(...)
    adapter.delete(...)
    # На commit: все успех, на exception: откат всего

# Клиент не координирует begin/commit/rollback вручную!
```

### 4. **Java Collections.sort()**
```java
// Фасад скрывает сложность сортировки:
Collections.sort(list);

// На самом деле:
// - Выбор алгоритма (quicksort, merge sort, insertion sort)
// - Компаратривание элементов
// - Разбиение на подмассивы
// - Рекурсивная сортировка
// Но пользователь просто вызывает sort()!
```

---

## 📝 Заключение

**Facade паттерн** решает проблему сложности:

1. **Делает API простым** – один метод вместо 20
2. **Скрывает деталей** – клиент не знает о подсистемах
3. **Обеспечивает безопасность** – правильный порядок операций гарантирован
4. **Упрощает тестирование** – можно мокировать подсистемы
5. **Облегчает поддержку** – изменяем подсистемы без влияния на клиентов

```
Key Idea: Создать единую точку входа к сложной подсистеме

Без Facade: Клиент должен думать как координировать (сложно + ошибки)
С Facade:   Клиент просто вызывает метод (просто + надёжно)
```

Фасад буквально как фасад здания – красивый однообразный вход, а за ним – сложная архитектура! 🏛️✨
