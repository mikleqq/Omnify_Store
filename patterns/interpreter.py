from abc import ABC, abstractmethod
from typing import Any─

class Context:
    
    def __init__(self, variables: dict = None):
        self.variables = variables or {}
    
    def set_variable(self, name: str, value: Any):
        self.variables[name] = value
    
    def get_variable(self, name: str) -> Any:
        return self.variables.get(name)
    
    def has_variable(self, name: str) -> bool:
        return name in self.variables

class AbstractExpression(ABC):
    
    @abstractmethod
    def interpret(self, context: Context) -> Any:

class TerminalExpression(AbstractExpression):
    
    def __init__(self, value: str):
        self.value = value
    
    def interpret(self, context: Context) -> Any:
        if context.has_variable(self.value):
            return context.get_variable(self.value)
        
        try:
            return float(self.value)
        except ValueError:
            pass
        
        return self.value

class BinaryExpression(AbstractExpression):
    
    def __init__(self, left: AbstractExpression, right: AbstractExpression):
        self.left = left
        self.right = right
    
    @abstractmethod
    def interpret(self, context: Context) -> Any:
        ...

class AddExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> float:
    
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return float(left_value) + float(right_value)

class SubtractExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> float:
    
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return float(left_value) - float(right_value)

class MultiplyExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> float:
    
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return float(left_value) * float(right_value)

class DivideExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> float:
    
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        right_float = float(right_value)
        if right_float == 0:
            raise ValueError("Деление на ноль")
        return float(left_value) / right_float

class GreaterThanExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> bool:
    
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return float(left_value) > float(right_value)

class LessThanExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> bool:
    
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return float(left_value) < float(right_value)

class EqualsExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> bool:
    
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return str(left_value).lower() == str(right_value).lower()

class AndExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> bool:
    
        left_result = self.left.interpret(context)
        right_result = self.right.interpret(context)
        return bool(left_result) and bool(right_result)

class OrExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> bool:
    
        left_result = self.left.interpret(context)
        right_result = self.right.interpret(context)
        return bool(left_result) or bool(right_result)

class PercentageExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> float:
    
        base_value = self.left.interpret(context)
        percent_value = self.right.interpret(context)
        return float(base_value) * (float(percent_value) / 100)

class MaxExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> float:
    
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return max(float(left_value), float(right_value))

class MinExpression(BinaryExpression):

    
    def interpret(self, context: Context) -> float:
    
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        return min(float(left_value), float(right_value))

class ExpressionBuilder:

    
    def __init__(self, expression_str: str):
        self.expression_str = expression_str.replace(" ", "")
        self.pos = 0
    
    def parse(self) -> AbstractExpression:
    
        return self._parse_or()
    
    def _parse_or(self) -> AbstractExpression:
    
        left = self._parse_and()
        
        while self.pos < len(self.expression_str) and self.expression_str[self.pos:self.pos+2] == "||":
            self.pos += 2
            right = self._parse_and()
            left = OrExpression(left, right)
        
        return left
    
    def _parse_and(self) -> AbstractExpression:
    
        left = self._parse_comparison()
        
        while self.pos < len(self.expression_str) and self.expression_str[self.pos:self.pos+2] == "&&":
            self.pos += 2
            right = self._parse_comparison()
            left = AndExpression(left, right)
        
        return left
    
    def _parse_comparison(self) -> AbstractExpression:
    
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
    
        if self.pos >= len(self.expression_str):
            raise ValueError("Неожиданный конец выражения")
        
        if self.expression_str[self.pos] == "(":
            self.pos += 1
            expr = self._parse_or()
            if self.pos >= len(self.expression_str) or self.expression_str[self.pos] != ")":
                raise ValueError("Ожидается закрывающая скобка")
            self.pos += 1
            return expr
        
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

def evaluate_expression(expression_str: str, context: Context) -> Any:

    builder = ExpressionBuilder(expression_str)
    ast = builder.parse()
    return ast.interpret(context)

def evaluate_filter(filter_expr: str, context: Context) -> bool:

    builder = ExpressionBuilder(filter_expr)
    ast = builder.parse()
    result = ast.interpret(context)
    return bool(result)
