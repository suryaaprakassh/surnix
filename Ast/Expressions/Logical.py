from Ast.Expressions.Expr import Expr
class Logical(Expr):
    
    def __init__(self, left, operator, right, ):
        self.left = left
        self.operator = operator
        self.right = right


    def accept(self, visitor):
        return visitor.visit_Logical(self)


