from Visitor import Visitor
from Token import TokenType
from Environment import Environment


class Interpreter(Visitor):

    environment = Environment()

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

    def __execute_block(self, statements, environment):
        previous = Interpreter.environment
        try:
            Interpreter.environment = environment
            for statement in statements:
                self.__evaluate(statement)
        finally:
            Interpreter.environment = previous

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

    def interpret(self, statements):
        from Surnix import Surnix
        try:
            for statement in statements:
                self.__evaluate(statement)
        except RuntimeError as e:
            Surnix.runtime_error(e)

    def visit_Expression(self, expr):
        self.__evaluate(expr.expression)
        return None

    def visit_Print(self, expr):
        value = self.__evaluate(expr.expression)
        print(self.__stringify(value))
        return None

    def visit_Var(self, expr):
        value = None
        if expr.initializer:
            value = self.__evaluate(expr.initializer)
        Interpreter.environment.define(expr.name, value)
        return None

    def visit_Variable(self, expr):
        return Interpreter.environment.get(expr.name)

    def visit_Block(self, expr):
        self.__execute_block(
            expr.statements, Environment(Interpreter.environment))
        return None

    def visit_Assign(self, expr):
        value = self.__evaluate(expr.value)

        Interpreter.environment.assign(expr.name, value)

        return value

    def visit_If(self, expr):
        if (self.__is_truthy(self.__evaluate(expr.condition))):
            self.__evaluate(expr.thenBranch)
        elif (expr.elseBranch):
            self.__evaluate(expr.elseBranch)
        return None
