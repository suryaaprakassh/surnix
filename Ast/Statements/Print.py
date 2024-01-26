from Ast.Statements.Stmt import Stmt

class Print(Stmt):
    def __init__(self, expression, ):
        self.expression = expression


    def accept(self, visitor):
        return visitor.visit_Print(self)


