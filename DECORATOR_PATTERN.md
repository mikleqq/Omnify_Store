# 🎨 Паттерн Decorator – Полная Документация

## 📋 Структура (по диаграмме)

```
              Component
             Operation()
                  △
                  │
        ┌─────────┴─────────┐
        │                   │
   ConcreteComponent    Decorator
                       (contains component)
                           △
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
  ConcreteDecoratorA              ConcreteDecoratorB
  Operation()                     Operation()
  addedState()                    addedBehavior()
```

## 🔑 Ключевые Компоненты

### 1. **Component (Интерфейс)**

```python
class Component(ABC):
    """Определяет интерфейс для объектов, которым могут добавляться обязанности."""
    
    @abstractmethod
    def operation(self) -> str:
        ...
```

**Назначение**: Единый интерфейс для конкретных компонентов и декораторов.

---

### 2. **ConcreteComponent (Конкретный компонент)**

```python
class ConcreteComponent(Component):
    """Конкретный объект, к которому добавляются обязанности."""
    
    def operation(self) -> str:
        return "ConcreteComponent"
```

**Назначение**: Базовый объект без дополнительных функций.

---

### 3. **Decorator (Абстрактный декоратор)** – КЛЮЧЕВОЙ КЛАСС

```python
class Decorator(Component):
    """Абстрактный декоратор.
    
    КЛЮЧЕВАЯ ОСОБЕННОСТЬ:
    - Содержит ссылку на Component (может быть компонент или декоратор)
    - Реализует тот же интерфейс Component
    - Делегирует операцию хранящемуся компоненту
    """
    
    def __init__(self, component: Component):
        self._component = component  # ← СВЯЗЬ: ссылка на компонент
    
    def operation(self) -> str:
        return self._component.operation()  # ← ДЕЛЕГИРОВАНИЕ
```

**Ключевэ моменты:**
- 🔗 **Содержит компонент** (`self._component`)
- 📦 **Может оборачивать как Component, так и Decorator**
- 🎯 **Реализует тот же интерфейс**
- 🔄 **Делегирует операцию компоненту**

---

### 4. **ConcreteDecoratorA/B (Конкретные декораторы)**

```python
class ConcreteDecoratorA(Decorator):
    """Конкретный декоратор A.
    
    Добавляет дополнительное поведение перед/после
    операции сохраняемого компонента.
    """
    
    def operation(self) -> str:
        # 1. Вызываем операцию компонента
        result = self._component.operation()
        
        # 2. Добавляем новое поведение
        added_behavior = "ConcreteDecoratorA: addedBehavior()"
        
        # 3. Объединяем результаты
        return f"{result}{{{added_behavior}}}"
    
    def add_state(self) -> str:
        """Дополнительная функциональность только в этом декораторе."""
        return "Added State from ConcreteDecoratorA"
```

**Назначение**: Добавляет конкретное поведение к компоненту.

---

## 🎯 Как Работает Decorator

### Без Decorator (Плохо ❌)

```python
# Нужны отдельные классы для каждой комбинации
class SimpleComponent: ...
class ComponentWithGift: ...
class ComponentWithExpress: ...
class ComponentWithGiftAndExpress: ...
class ComponentWithGiftAndExpressAndInsurance: ...
# ... экспоненциальный рост!
```

### С Decorator (Хорошо ✅)

```python
# Один базовый компонент + несколько декораторов
base = ConcreteComponent()

# Строим комбинацию как матрёшка!
decorated = ConcreteDecoratorA(base)
decorated = ConcreteDecoratorB(decorated)

# Каждый декоратор знает о одной функции, остальное делегирует

# Рекурсия в операциях:
decorated.operation()
  → ConcreteDecoratorB.operation()
      → adds behavior "B"
      → calls self._component.operation()
          → ConcreteDecoratorA.operation()
              → adds behavior "A"
              → calls self._component.operation()
                  → ConcreteComponent.operation()
                      → returns "Component"
```

---

## 📊 Поток Выполнения: Пример с Заказами

### Создание декорированного заказа:

```python
# Шаг 1: Базовый заказ
base = BaseOrder(items=[...], delivery_cost=100)
# Стоимость: $1000 + $100 доставка = $1100

# Шаг 2: Добавляем подарочную упаковку
step1 = GiftWrapDecorator(base)
# Стоимость: $1100 + $150 упаковка = $1250

# Шаг 3: Добавляем ускоренную доставку
step2 = ExpressUpgradeDecorator(step1)
# Стоимость: $1250 + $300 ускорение = $1550

# Шаг 4: Добавляем страховку
step3 = InsuranceDecorator(step2)
# Стоимость: $1550 + 1% = $1565.50

# Шаг 5: Применяем скидку 10%
final = DiscountDecorator(step3, 10)
# Стоимость: $1565.50 × 0.9 = $1408.95

# Итоговая стоимость при вызове get_cost():
final.get_cost()  → Проходит цепочку всех декораторов!
```

### Цепочка делегирования при вызове `get_cost()`:

```
DiscountDecorator.get_cost()
  → $1565.50 × 0.9 = $1408.95
  → calls self._component.get_cost()
      → InsuranceDecorator.get_cost()
          → $1550 + 1% = $1565.50
          → calls self._component.get_cost()
              → ExpressUpgradeDecorator.get_cost()
                  → $1250 + $300 = $1550
                  → calls self._component.get_cost()
                      → GiftWrapDecorator.get_cost()
                          → $1100 + $150 = $1250
                          → calls self._component.get_cost()
                              → BaseOrder.get_cost()
                                  → $1100 (базовая стоимость)
```

---

## ✨ Преимущества Decorator

| Преимущество | Объяснение |
|---|---|
| **Гибкость** | Комбинируй декораторы любыми способами |
| **Открыт/Закрыт** | Открыт для расширения (новые декораторы), закрыт для модификации |
| **Единая ответственность** | Каждый декоратор отвечает за одно |
| **Динамическое расширение** | Добавляй функции в runtime |
| **Избегаем взрывной иерархии** | Не нужны классы для каждой комбинации |
| **Композиция вместо наследования** | Более гибко, чем подтипы |

---

## ❌ Недостатки Decorator

| Проблема | Описание |
|---|---|
| **Сложность** | Порядок декораторов может быть важным |
| **Отладка** | Трудно отследить цепочку вызовов |
| **Производительность** | Цепочка вызовов может быть медленной |
| **Сложность типов** | Тип хранящегося объекта может быть неопределён |

---

## 🔄 Сравнение с Похожими Паттернами

| Паттерн | Назначение | Когда использовать |
|---------|-----------|-------------------|
| **Decorator** | Динамич. добавление функций | Runtime опции, комбинируемые функции |
| **Strategy** | Выбрать алгоритм | Один способ выполнения операции |
| **Composite** | Древовидная структура | Иерархия объектов |
| **Adapter** | Адаптировать интерфейс | Несовместимые интерфейсы |
| **Proxy** | Контролировать доступ | Ленивая инициализация, логирование |

---

## 🎯 Когда Использовать Decorator

✅ **Используйте когда:**

1. **Динамическое добавление функций**
   - Нужно добавлять функции в runtime
   - Не хотите их знать заранее

2. **Комбинируемые функции**
   - Функции можно смешивать и комбинировать
   - Порядок применения может быть важным

3. **Избегаете взрывной иерархии**
   - Вместо A×B комбинаций классов: используйте A+B декораторов

4. **Единая ответственность**
   - Каждая функция в отдельном декораторе

❌ **НЕ используйте когда:**

1. **Функция не комбинируется**
   - Есть только одна функция
   - Используйте наследование

2. **Производительность критична**
   - Цепочка вызовов может быть узким местом

3. **Простая иерархия**
   - Всего 2-3 варианта
   - Просто наследуйте

---

## 💻 Практический Пример: Система Заказов

```python
# Создаём базовый заказ
items = [
    {"name": "Laptop", "price": 1000, "quantity": 1},
]
order = BaseOrder(items, delivery_cost=100)

# Применяем декораторы
decorators = ["gift_wrap", "express", "insurance"]
fancy_order = apply_decorators(order, decorators, discount_pct=10)

# Используем декорированный заказ
print(fancy_order.get_cost())        # $1408.95
print(fancy_order.get_description()) # "Заказ... + упаковка + ускорение + страховка – скидка 10%"

# Получаем список опций
extras = get_extras(fancy_order)
# [
#   {"name": "Подарочная упаковка", "icon": "🎁", "cost": 150},
#   {"name": "Ускоренная обработка", "icon": "⚡", "cost": 300},
#   {"name": "Страховка груза", "icon": "🛡️", "cost": ...},
#   {"name": "Скидка 10%", "icon": "🏷️", "cost": -156.55}
# ]
```

---

## 🔍 Анализ Структуры

### Главная идея: ЛЯД вместо наследования

```
Наследование (плохо):
────────────────────
class SimpleOrder: ...
class OrderWithGift(SimpleOrder): ...
class OrderWithExpress(SimpleOrder): ...
class OrderWithGiftAndExpress(OrderWithGift): ...
# Экспоненциальный рост!

Decorator (хорошо):
───────────────────
class BaseOrder: ...
class GiftWrapDecorator(Decorator): ...  # Оборачивает Order или другой Decorator
class ExpressDecorator(Decorator): ...   # Оборачивает Order или другой Decorator

# Комбинируем как нужно в runtime!
order = ExpressDecorator(GiftWrapDecorator(BaseOrder(...)))
```

---

## 🚀 Распространённые Применения

### 1. **Система заказов** (в этом проекте)
- Опции заказа (упаковка, доставка, страховка)
- Скидки и акции

### 2. **I/O Streams** (Java)
```python
# Аналог Java: new GZIPInputStream(new BufferedInputStream(fileStream))
stream = GZIPDecorator(BufferedDecorator(FileStream("file.txt")))
```

### 3. **UI Компоненты** (в графических фреймворках)
```
Button → WithBorder → WithBackgroundColor → WithShadow
```

### 4. **Логирование и Мониторинг**
```
DatabaseConnection → WithLogging → WithMetrics → WithCaching
```

### 5. **Валидация данных**
```
Input → TrimWhitespace → ValidateEmail → SanitizeSQL → ProcessData
```

---

## 📚 Файлы в Проекте

### [patterns/decorator.py](patterns/decorator.py)

Содержит:
- **Базовые классы** (по диаграмме):
  - `Component` – интерфейс
  - `ConcreteComponent` – базовый компонент
  - `Decorator` – абстрактный декоратор
  - `ConcreteDecoratorA`, `ConcreteDecoratorB` – конкретные декораторы

- **Система заказов** (применение паттерна):
  - `OrderComponent`, `BaseOrder` – интерфейс и базовый заказ
  - `OrderDecorator` – абстрактный декоратор заказа
  - `GiftWrapDecorator`, `ExpressUpgradeDecorator`, `InsuranceDecorator`, `DiscountDecorator` – конкретные опции

- **Утилиты**:
  - `apply_decorators()` – применить несколько декораторов
  - `get_extras()` – получить список опций

---

## 📝 Заключение

**Decorator паттерн** позволяет:

1. **Динамически добавлять функции** к объектам в runtime
2. **Комбинировать функции** без создания всех возможных комбинаций явно
3. **Избегать наследования** через композицию
4. **Сохранять чистоту кода** благодаря единой ответственности

```
Key Idea: Обеспечить гибкость посредством композиции вместо наследования

Без Decorator:  2 свойства × 3 значения = 6 классов
С Decorator:    2 свойства + 3 значения = 5 классов
```

Это буквально "украшение" объекта новой функциональностью! 🎨✨
