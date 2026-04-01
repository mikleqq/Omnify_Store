# 🎨 Паттерн Adapter – Полная Документация

## 📋 Структура (по диаграмме DrawingEditor)

```
┌─────────────────────────────────────────────────────┐
│           DrawingEditor (Клиент)                    │
│  • add_shape(shape)                                 │
│  • set_selected_shape(shape) → Manipulator          │
│  • get_all_bounds() → list[dict]                    │
│  • get_shape_info() → list[dict]                    │
└──────────────────┬──────────────────────────────────┘
                   │ работает только с
                   ↓
        ┌──────────────────────┐
        │   Shape (Interface)  │
        │  • bounding_box()    │
        │  • create_manipulator│
        └──────────┬───────────┘
                   │
          ┌────────┴────────┐
          ↓                 ↓
   ┌─────────────┐  ┌──────────────────────┐
   │   Line      │  │  TextShape (Adapter) │
   │ (встроенная │  │  • содержит TextView │
   │  реализ.)   │  │  • адаптирует API    │
   └─────────────┘  └──────────┬───────────┘
                               │ адаптирует
                               ↓
                        ┌──────────────────┐
                        │  TextView        │
                        │ (Adaptee)        │
                        │ • get_extent()   │
                        │ • set_origin()   │
                        └──────────────────┘
```

## 🔑 Ключевые Компоненты

### 1. **Target Interface (Целевой интерфейс)**

```python
class Shape(ABC):
    @abstractmethod
    def bounding_box() -> dict:
        """Возвращает границы фигуры в формате {x, y, width, height}"""
    
    @abstractmethod
    def create_manipulator() -> Manipulator:
        """Создаёт манипулятор для управления фигурой"""
```

**Назначение**: Определяет интерфейс, с которым работает клиент (DrawingEditor).

---

### 2. **Concrete Shapes (Конкретные реализации)**

#### Line (Встроенная реализация)
```python
class Line(Shape):
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
    
    def bounding_box() -> dict:
        # Встроенная реализация, никакой адаптации не нужно
    
    def create_manipulator() -> LineManipulator:
        return LineManipulator(self)
```

**Назначение**: Реализует интерфейс Shape с встроенной логикой.

---

### 3. **Adaptee (Адаптируемый класс)**

```python
class TextView:  # НЕСОВМЕСТИМЫЙ ИНТЕРФЕЙС
    def __init__(self, text: str):
        self.text = text
        self._origin_x = 0
        self._origin_y = 0
        self._width = len(text) * 8
        self._height = 16
    
    def get_extent() -> dict:
        # НЕСОВМЕСТИМЫЙ метод (вместо bounding_box())
        return {
            "origin_x": ...,   # вместо "x"
            "origin_y": ...,   # вместо "y"
            "width": ...,
            "height": ...
        }
    
    def set_origin(x: int, y: int) -> None:
        # НЕСОВМЕСТИМЫЙ метод позиционирования
```

**Проблема**: 
- Использует `get_extent()` вместо `bounding_box()`
- Использует `origin_x/origin_y` вместо `x/y`
- Несовместим с интерфейсом Shape

---

### 4. **Adapter (Адаптер) – ГЛАВНЫЙ КОМПОНЕНТ**

```python
class TextShape(Shape):  # НАСЛЕДУЕТ целевой интерфейс
    def __init__(self, text_view: TextView):
        self._text_view = text_view  # СОДЕРЖИТ адаптируемый объект
    
    def bounding_box(self) -> dict:
        # АДАПТИРУЕТ несовместимый API к целевому интерфейсу
        extent = self._text_view.get_extent()
        return {
            "x": extent["origin_x"],        # Преобразование имен
            "y": extent["origin_y"],        # origin_x → x
            "width": extent["width"],       # origin_y → y
            "height": extent["height"],
        }
    
    def create_manipulator(self) -> Manipulator:
        # АДАПТИРУЕТ для работы с manpulyator API
        return TextManipulator(self._text_view)
```

**Как это работает**:
1. **Наследует** целевой интерфейс Shape
2. **Содержит** объект несовместимого класса (TextView)
3. **Преобразует** методы:
   - `bounding_box()` → `get_extent()`
   - `origin_x/origin_y` → `x/y`
4. **Преобразует** данные между несовместимыми форматами

---

### 5. **Manipulator Hierarchy (Иерархия манипуляторов)**

```python
class Manipulator(ABC):
    @abstractmethod
    def handle_mouse_down(x, y) -> None: ...
    @abstractmethod
    def handle_mouse_drag(x, y) -> None: ...
    @abstractmethod
    def handle_mouse_up(x, y) -> None: ...
    @abstractmethod
    def get_info() -> dict: ...

class LineManipulator(Manipulator):
    # Управляет Line напрямую
    
class TextManipulator(Manipulator):
    # Управляет TextView через адаптер
```

---

## 🔄 Поток Выполнения

```python
# Сценарий использования:
editor = DrawingEditor()

# 1. Добавляем обычную линию (встроенная реализация)
line = Line(10, 20, 100, 50)
editor.add_shape(line)

# 2. Создаём несовместимый TextView
text_view = TextView("Hello")

# 3. Адаптируем его через TextShape
text_shape = TextShape(text_view)  # ← ADAPTER
editor.add_shape(text_shape)

# 4. DrawingEditor работает с обоими как с Shape
bounds = editor.get_all_bounds()  # Работает для Line и TextShape

# 5. Выбираем фигуру и получаем манипулятор
manipulator = editor.set_selected_shape(text_shape)
# → Возвращает TextManipulator, который работает с TextView

# 6. Управляем фигурой
manipulator.handle_mouse_down(50, 60)
manipulator.handle_mouse_drag(100, 80)
manipulator.handle_mouse_up(100, 80)
# → TextManipulator транслирует в методы TextView.set_origin()
```

---

## ✅ Advantages / Преимущества

| Преимущество | Описание |
|---|---|
| **Разделение ответственности** | Клиент не знает о несовместимости |
| **Переиспользование кода** | Можно использовать TextView без изменений |
| **Гибкость** | Легко добавить новые адаптеры |
| **Открыт/Закрыт принцип** | Можно адаптировать новые классы без изменения существующих |
| **Инкапсуляция** | Преобразование интерфейса скрыто в адаптере |

---

## ❌ Недостатки / Антипаттерны

| Проблема | Решение |
|---|---|
| **Слишком много адаптеров** | Может указывать на плохой дизайн исходных классов |
| **Сложные преобразования** | Сигнал к переработке интерфейсов |
| **Множество оберток** | Усложняет отладку |

---

## 🎯 Когда Использовать

✅ **Используйте Adapter когда:**
- Нужно использовать класс с несовместимым интерфейсом
- Нельзя или не хотите менять исходный класс
- Нужна унификация интерфейсов разных систем
- Интегрируете сторонние библиотеки

❌ **НЕ используйте когда:**
- Можно изменить интерфейс исходного класса
- Преобразование слишком сложное
- Это добавляет ненужную сложность

---

## 📊 Сравнение с другими паттернами

| Паттерн | Назначение | Когда использовать |
|---------|-----------|-------------------|
| **Adapter** | Адаптирует несовместимый интерфейс | Сторонние библиотеки |
| **Decorator** | Добавляет функциональность | Расширение без изменения |
| **Facade** | Упрощает сложный интерфейс | Группировка операций |
| **Bridge** | Разделяет абстракцию и реализацию | Независимая эволюция |

---

## 💡 Практический Пример: Платежные Системы

В том же файле `adapter.py` реализована вторая версия паттерна для платежей:

```python
# Несовместимые API
class StripeAPILegacy:
    def create_charge(amount_cents, ...) -> dict  # Несовместимо

class PayPalSDKLegacy:
    def execute_payment(payer_id, ...) -> dict    # Несовместимо

# Адаптер
class StripeAdapter(PaymentProcessor):
    def __init__(self):
        self._stripe = StripeAPILegacy()
    
    def process_payment(amount, details) -> dict:
        # Адаптирует create_charge() к process_payment()
        result = self._stripe.create_charge(
            amount_cents=int(amount * 100),
            ...
        )
        return {"success": ..., "transaction_id": ...}

# Использование
adapter = get_payment_adapter("card")  # Получить адаптер
result = adapter.process_payment(100.0, {...})  # Работает!
```

---

## 📚 Файлы в Проекте

- **`patterns/adapter.py`** — Полная реализация с двумя примерами:
  1. Shape/TextView/TextShape (основной пример из диаграммы)
  2. PaymentProcessor/StripeAdapter (доп. пример)

- **`patterns/adapter_demo.py`** — Демонстрация работы паттерна

- **`app.py`** — Использует `get_payment_adapter()` при оформлении платежей

---

## 🚀 Запуск Демонстрации

```bash
cd /workspaces/Omnify_Store
python -m patterns.adapter_demo
```

**Вывод показывает:**
- Добавление Line и TextShape в DrawingEditor
- Получение границ обеих фигур (несмотря на разные API)
- Работу манипуляторов для обеих фигур
- Полную информацию о фигурах

---

## 📝 Заключение

Паттерн **Adapter** позволяет:
1. **Адаптировать** несовместимые интерфейсы
2. **Переиспользовать** существующие классы
3. **Унифицировать** работу с разными системами
4. **Раскрывать** интерфейсы через адаптацию

Это один из самых практичных паттернов в реальной разработке! ✨
