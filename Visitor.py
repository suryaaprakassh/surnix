from abc import abstractmethod
from abc import abstractmethod, ABC
from typing import Any


class Visitor(ABC):
    @abstractmethod
    def visit_Binary(self, expr)->Any:
        pass

    @abstractmethod
    def visit_Grouping(self, expr):
        pass

    @abstractmethod
    def visit_Literal(self, expr)-> str:
        pass

    @abstractmethod
    def visit_Unary(self, expr)->Any:
        pass

    @abstractmethod
    def visit_Variable(self, expr):
        pass

    @abstractmethod
    def visit_Expression(self, expr):
        pass

    @abstractmethod
    def visit_Print(self, expr):
        pass

    @abstractmethod
    def visit_Var(self, expr):
        pass

    @abstractmethod
    def visit_Block(self, expr):
        pass

    @abstractmethod
    def visit_Assign(self, expr):
        pass

    @abstractmethod
    def visit_If(self, expr):
        pass
    
    @abstractmethod
    def visit_Logical(self,expr):
        pass
    @abstractmethod
    def visit_While(self,expr):
        pass
