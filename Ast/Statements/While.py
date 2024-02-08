from Ast.Statements.Stmt import Stmt

class While(Stmt):
    def __init__(self, condition, body ):
        self.condition= condition
        self.body= body

    def accept(self, visitor):
        return visitor.visit_While(self)


