from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Environment:
    values: Dict[str, Any] = field(default_factory=dict)

    def define(self, name: str, value: object):
        self.values[name.lexeme] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise RuntimeError(name, f"Undefined Variable {name.lexeme} .")
