from Visitor import Visitor
from Token import TokenType


class Interpreter(Visitor):
    def visit_Literal(self, expr):
        return expr.value

    def __evaluate(self, expr):
        return expr.accept(self)

    def __is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def __check_number_operand(self, operator, *operands):
        for operand in operands:
            if not isinstance(operand, float):
                raise RuntimeError(f"Operand must be a number. {operator}")
        return

    def visit_Grouping(self, expr):
        return self.__evaluate(expr.expression)

    def visit_Unary(self, expr):
        right = self.__evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            self.__check_number_operand(expr.operator, right)
            return -right
        elif expr.operator.type == TokenType.BANG:
            return not self.__is_truthy(right)
        return None

    def __is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def visit_Binary(self, expr):
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.__check_number_operand(expr.operator, left, right)
                return left - right
            case TokenType.SLASH:
                self.__check_number_operand(expr.operator, left, right)
                return left / right
            case TokenType.STAR:
                self.__check_number_operand(expr.operator, left, right)
                return left * right
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    self.__check_number_operand(expr.operator, left, right)
                    return left + right
                elif isinstance(left, str) and isinstance(right, str):
                    return left + right
                else:
                    raise RuntimeError(
                        "Operands must be two numbers or two strings.")
            case TokenType.GREATER:
                self.__check_number_operand(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.__check_number_operand(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.__check_number_operand(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.__check_number_operand(expr.operator, left, right)
                return left <= right
            case TokenType.BANG_EQUAL:
                return not self.__is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.__is_equal(left, right)

    def __stringify(self, obj):
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)

    def interpret(self, expr):
        try:
            value = self.__evaluate(expr)
            print(self.__stringify(value))
        except RuntimeError as e:
            print(e)
