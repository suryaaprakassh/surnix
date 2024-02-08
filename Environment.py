from typing import Dict, Any


class Environment:
    def __init__(self, enclosing=None) -> None:
        self.values: Dict[str, Any] = dict()
        self.enclosing = enclosing

    def define(self, name, value: object):
        self.values[name.lexeme] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        raise RuntimeError(name, f"Undefined Variable {name.lexeme} .")

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name,value) 
            return 
        raise Exception(f"Undefined variable {name.lexeme}.")
