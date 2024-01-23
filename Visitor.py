from abc import ABC, abstractmethod


class Visitor(ABC):
    @abstractmethod
    def visit_Binary(self, expr):
        pass

    @abstractmethod
    def visit_Grouping(self, expr):
        pass

    @abstractmethod
    def visit_Literal(self, expr):
        pass

    @abstractmethod
    def visit_Unary(self, expr):
        pass
