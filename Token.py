from TokenType import TokenType


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"Token({self.type}, {self.lexeme})"

    def __repr__(self):
        return self.__str__()
