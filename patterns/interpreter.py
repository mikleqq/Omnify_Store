# ─────────────────────────────────────────────
#  INTERPRETER  –  интерпретатор выражений
# ─────────────────────────────────────────────
#
#  Структура:
#  - AbstractExpression (базовое выражение с методом interpret(context))
#  - TerminalExpression (терминальное выражение)
#  - NonterminalExpression (нетерминальное выражение с ссылками на другие)
#  - Context (контекст для интерпретации)
#  - Client (строит AST и вызывает interpret)
#

from abc import ABC, abstractmethod
from typing import Any


# ── CONTEXT ──────────────────────────────────

class Context:
    """
    Context - контекст
    Содержит информацию, необходимую для интерпретации
    """
    
    def __init__(self, variables: dict = None):
        self.variables = variables or {}
    
    def set_variable(self, name: str, value: Any):
        """Устанавливает переменную"""
        self.variables[name] = value
    
    def get_variable(self, name: str) -> Any:
        """Получает значение переменной"""
        return self.variables.get(name)
    
    def has_variable(self, name: str) -> bool:
        """Проверяет наличие переменной"""
        return name in self.variables


# ── ABSTRACT EXPRESSION ──────────────────────

class AbstractExpression(ABC):
    """
    AbstractExpression (Regular Expression)
    Абстрактное выражение - определяет интерфейс для интерпретации
    """
    
    @abstractmethod
    def interpret(self, context: Context) -> Any:
        """Interpret(context) - интерпретирует выражение в контексте"""
        ...


# ── TERMINAL EXPRESSION ──────────────────────

class TerminalExpression(AbstractExpression):
    """
    TerminalExpression
    Терминальное выражение - реализует операции интерпретации для терминальных элементов
    """
    
    def __init__(self, value: str):
        self.value = value
    
    def interpret(self, context: Context) -> Any:
        """Interpret(context) - интерпретирует терминальное выражение"""
        # Пытаемся получить переменную из контекста
        if context.has_variable(self.value):
            return context.get_variable(self.value)
        
        # Попытка преобразовать в число
        try:
            return float(self.value)
        except ValueError:
            pass
        
        # Иначе вернуть строку как есть
        return self.value


# ── NONTERMINAL EXPRESSIONS ─────────────────

class BinaryExpression(AbstractExpression):
    """
    NonterminalExpression (AlternativeExpression, RepetitionExpression, SequenceExpression)
    Нетерминальное выражение - содержит ссылки на другие выражения
    """
    
    def __init__(self, left: AbstractExpression, right: AbstractExpression):
        self.left = left
        self.right = right
    
    @abstractmethod
    def interpret(self, context: Context) -> Any:
        ...


class AddExpression(BinaryExpression):
    """Нетерминальное выражение: сложение"""
    
    def interpret(self, context: Context) -> float:
        """Interpret(context) - рекурсивно интерпретирует левое и правое выражения"""
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return float(left_value) + float(right_value)


class SubtractExpression(BinaryExpression):
    """Нетерминальное выражение: вычитание"""
    
    def interpret(self, context: Context) -> float:
        """Interpret(context) - рекурсивно интерпретирует левое и правое выражения"""
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return float(left_value) - float(right_value)


class MultiplyExpression(BinaryExpression):
    """Нетерминальное выражение: умножение"""
    
    def interpret(self, context: Context) -> float:
        """Interpret(context) - рекурсивно интерпретирует левое и правое выражения"""
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return float(left_value) * float(right_value)


class DivideExpression(BinaryExpression):
    """Нетерминальное выражение: деление"""
    
    def interpret(self, context: Context) -> float:
        """Interpret(context) - рекурсивно интерпретирует левое и правое выражения"""
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        right_float = float(right_value)
        if right_float == 0:
            raise ValueError("Деление на ноль")
        return float(left_value) / right_float


class GreaterThanExpression(BinaryExpression):
    """Нетерминальное выражение: больше чем"""
    
    def interpret(self, context: Context) -> bool:
        """Interpret(context) - рекурсивно интерпретирует и сравнивает"""
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return float(left_value) > float(right_value)


class LessThanExpression(BinaryExpression):
    """Нетерминальное выражение: меньше чем"""
    
    def interpret(self, context: Context) -> bool:
        """Interpret(context) - рекурсивно интерпретирует и сравнивает"""
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return float(left_value) < float(right_value)


class EqualsExpression(BinaryExpression):
    """Нетерминальное выражение: равно"""
    
    def interpret(self, context: Context) -> bool:
        """Interpret(context) - рекурсивно интерпретирует и сравнивает"""
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return str(left_value).lower() == str(right_value).lower()


class AndExpression(BinaryExpression):
    """Нетерминальное выражение: логическое И"""
    
    def interpret(self, context: Context) -> bool:
        """Interpret(context) - рекурсивно интерпретирует оба выражения"""
        left_result = self.left.interpret(context)
        right_result = self.right.interpret(context)
        return bool(left_result) and bool(right_result)


class OrExpression(BinaryExpression):
    """Нетерминальное выражение: логическое ИЛИ"""
    
    def interpret(self, context: Context) -> bool:
        """Interpret(context) - рекурсивно интерпретирует оба выражения"""
        left_result = self.left.interpret(context)
        right_result = self.right.interpret(context)
        return bool(left_result) or bool(right_result)


class PercentageExpression(BinaryExpression):
    """Нетерминальное выражение: процент"""
    
    def interpret(self, context: Context) -> float:
        """Interpret(context) - вычисляет процент: base * (percent / 100)"""
        base_value = self.left.interpret(context)
        percent_value = self.right.interpret(context)
        return float(base_value) * (float(percent_value) / 100)


class MaxExpression(BinaryExpression):
    """Нетерминальное выражение: максимум"""
    
    def interpret(self, context: Context) -> float:
        """Interpret(context) - возвращает максимум из двух значений"""
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return max(float(left_value), float(right_value))


class MinExpression(BinaryExpression):
    """Нетерминальное выражение: минимум"""
    
    def interpret(self, context: Context) -> float:
        """Interpret(context) - возвращает минимум из двух значений"""
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return min(float(left_value), float(right_value))


# ── CLIENT ───────────────────────────────────

class ExpressionBuilder:
    """
    Client - клиент
    Строит абстрактное синтаксическое дерево (AST) и вызывает interpret()
    """
    
    def __init__(self, expression_str: str):
        self.expression_str = expression_str.replace(" ", "")
        self.pos = 0
    
    def parse(self) -> AbstractExpression:
        """Строит AST из строкового выражения"""
        return self._parse_or()
    
    def _parse_or(self) -> AbstractExpression:
        """Парсит OR выражение (самый низкий приоритет)"""
        left = self._parse_and()
        
        while self.pos < len(self.expression_str) and self.expression_str[self.pos:self.pos+2] == "||":
            self.pos += 2
            right = self._parse_and()
            left = OrExpression(left, right)
        
        return left
    
    def _parse_and(self) -> AbstractExpression:
        """Парсит AND выражение"""
        left = self._parse_comparison()
        
        while self.pos < len(self.expression_str) and self.expression_str[self.pos:self.pos+2] == "&&":
            self.pos += 2
            right = self._parse_comparison()
            left = AndExpression(left, right)
        
        return left
    
    def _parse_comparison(self) -> AbstractExpression:
        """Парсит сравнения"""
        left = self._parse_additive()
        
        if self.pos < len(self.expression_str):
            if self.expression_str[self.pos:self.pos+2] == ">=":
                self.pos += 2
                right = self._parse_additive()
                return OrExpression(
                    GreaterThanExpression(left, right),
                    EqualsExpression(left, right)
                )
            elif self.expression_str[self.pos:self.pos+2] == "<=":
                self.pos += 2
                right = self._parse_additive()
                return OrExpression(
                    LessThanExpression(left, right),
                    EqualsExpression(left, right)
                )
            elif self.expression_str[self.pos] == ">":
                self.pos += 1
                right = self._parse_additive()
                return GreaterThanExpression(left, right)
            elif self.expression_str[self.pos] == "<":
                self.pos += 1
                right = self._parse_additive()
                return LessThanExpression(left, right)
            elif self.expression_str[self.pos] == "=":
                self.pos += 1
                right = self._parse_additive()
                return EqualsExpression(left, right)
        
        return left
    
    def _parse_additive(self) -> AbstractExpression:
        """Парсит сложение и вычитание"""
        left = self._parse_multiplicative()
        
        while self.pos < len(self.expression_str) and self.expression_str[self.pos] in "+-":
            op = self.expression_str[self.pos]
            self.pos += 1
            right = self._parse_multiplicative()
            if op == "+":
                left = AddExpression(left, right)
            else:
                left = SubtractExpression(left, right)
        
        return left
    
    def _parse_multiplicative(self) -> AbstractExpression:
        """Парсит умножение, деление и проценты"""
        left = self._parse_primary()
        
        while self.pos < len(self.expression_str) and self.expression_str[self.pos] in "*/%":
            op = self.expression_str[self.pos]
            self.pos += 1
            right = self._parse_primary()
            if op == "*":
                left = MultiplyExpression(left, right)
            elif op == "/":
                left = DivideExpression(left, right)
            else:  # %
                left = PercentageExpression(left, right)
        
        return left
    
    def _parse_primary(self) -> AbstractExpression:
        """Парсит первичное выражение (терминальное)"""
        if self.pos >= len(self.expression_str):
            raise ValueError("Неожиданный конец выражения")
        
        # Скобки
        if self.expression_str[self.pos] == "(":
            self.pos += 1
            expr = self._parse_or()
            if self.pos >= len(self.expression_str) or self.expression_str[self.pos] != ")":
                raise ValueError("Ожидается закрывающая скобка")
            self.pos += 1
            return expr
        
        # Число или переменная
        start = self.pos
        while self.pos < len(self.expression_str) and (
            self.expression_str[self.pos].isalnum() or 
            self.expression_str[self.pos] in "._"
        ):
            self.pos += 1
        
        if start == self.pos:
            raise ValueError(f"Неожиданный символ: {self.expression_str[self.pos]}")
        
        value = self.expression_str[start:self.pos]
        return TerminalExpression(value)


# ── ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ─────────────────

def evaluate_expression(expression_str: str, context: Context) -> Any:
    """
    Вычисляет выражение с помощью интерпретатора
    
    Args:
        expression_str: Строковое выражение (например, "price * 0.9")
        context: Контекст с переменными
    
    Returns:
        Результат интерпретации
    """
    builder = ExpressionBuilder(expression_str)
    ast = builder.parse()
    return ast.interpret(context)


def evaluate_filter(filter_expr: str, context: Context) -> bool:
    """
    Вычисляет условие фильтра
    
    Args:
        filter_expr: Строковое выражение (например, "price > 100 && quantity < 50")
        context: Контекст с переменными товара
    
    Returns:
        True или False
    """
    builder = ExpressionBuilder(filter_expr)
    ast = builder.parse()
    result = ast.interpret(context)
    return bool(result)
