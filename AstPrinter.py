from Visitor import Visitor


class AstPrinter(Visitor):

    def parenthesize(self, name, *exprs):
        return_string = "(" + name + " "

        for expr in exprs:
            return_string += " " + expr.accept(self)
        return_string += ")"

        return return_string

    def visit_Binary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_Grouping(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_Literal(self, expr):
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def visit_Unary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def print(self, expr):
        return expr.accept(self)


if __name__ == "__main__":
    from Token import Token
    from TokenType import TokenType
    from Unary import Unary
    from Literal import Literal
    from Grouping import Grouping
    from Binary import Binary

    expr = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )

    print(AstPrinter().print(expr))
