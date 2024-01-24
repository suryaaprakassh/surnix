from Expr import Expr

class Grouping(Expr):
    def __init__(self, expression, ):
        self.expression = expression


    def accept(self, visitor):
        return visitor.visit_Grouping(self)


