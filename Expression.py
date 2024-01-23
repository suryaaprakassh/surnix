from Stmt import Stmt

class Expression(Stmt):
    def __init__(self, expression, ):
        self.expression = expression


    def accept(self, visitor):
        return visitor.visit_Expression(self)


