from Expr import Expr


class Variable(Expr):
    def __init__(self, name, ):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_Variable(self)
