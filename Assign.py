from Expr import Expr

class Assign(Expr):
    def __init__(self, name, value, ):
        self.name = name
        self.value = value


    def accept(self, visitor):
        return visitor.visit_Assign(self)


