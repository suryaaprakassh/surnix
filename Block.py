from Stmt import Stmt

class Block(Stmt):
    def __init__(self, statements, ):
        self.statements = statements


    def accept(self, visitor):
        return visitor.visit_Block(self)


