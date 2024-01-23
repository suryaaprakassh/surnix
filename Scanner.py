from typing import List
from Token import Token
from TokenType import TokenType
from Surnix import Surnix


class Scanner:
    start = 0
    current = 0
    line = 1

    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: List[Token] = []

    def reset(self):
        Scanner.line = 1
        Scanner.current = 0
        Scanner.start = 0

    def __is_at_end(self) -> bool:
        return Scanner.current >= len(self.source)

    def scan_tokens(self) -> List[Token]:
        while (not self.__is_at_end()):
            Scanner.start = Scanner.current
            self.__scan_token()
            if (Surnix.had_error):
                break
        self.tokens.append(Token(TokenType.EOF, "", None, Scanner.line))
        return self.tokens

    def __advance(self) -> str:
        Scanner.current += 1
        return self.source[Scanner.current - 1]

    def __add_token_literal(self, token_type: TokenType, literal: object = None) -> None:
        text = self.source[Scanner.start:Scanner.current]
        self.tokens.append(Token(token_type, text, literal, Scanner.line))

    def __add_token(self, token_type: TokenType) -> None:
        self.__add_token_literal(token_type, None)

    def __match(self, expected: str) -> bool:
        if self.__is_at_end():
            return False
        if self.source[Scanner.current] != expected:
            return False
        Scanner.current += 1
        return True

    def __peek(self):
        if self.__is_at_end():
            return '\0'
        return self.source[Scanner.current]

    def __string(self):
        while not self.__is_at_end() and self.__peek() != '"':
            if self.__peek() == '\n':
                Scanner.line += 1
            self.__advance()
        if (self.__is_at_end()):
            Surnix.error(Scanner.line, "Unterminated string.")
            return
       # closing quote
        self.__advance()

        value = self.source[Scanner.start + 1:Scanner.current - 1]
        self.__add_token_literal(TokenType.STRING, value)

    def __peek_next(self):
        if Scanner.current+1 >= len(self.source):
            return '\0'
        return self.source[Scanner.current+1]

    def __number(self):
        while not self.__is_at_end() and self.__peek().isdigit():
            self.__advance()
        if self.__peek() == '.' and self.__peek_next().isdigit():
            self.__advance()
            while self.__peek().isdigit():
                self.__advance()
        self.__add_token_literal(TokenType.NUMBER, float(
            self.source[Scanner.start:Scanner.current]))

    def __identifier(self):
        while self.__peek().isalnum():
            self.__advance()
        text = self.source[Scanner.start:Scanner.current]
        token_type = Scanner.keywords.get(text, TokenType.IDENTIFIER)
        self.__add_token(token_type)

    def __scan_token(self):
        c = self.__advance()

        match c:
            case '(': self.__add_token(TokenType.LEFT_PAREN)
            case ')': self.__add_token(TokenType.RIGHT_PAREN)
            case '{': self.__add_token(TokenType.LEFT_BRACE)
            case '}': self.__add_token(TokenType.RIGHT_BRACE)
            case ',': self.__add_token(TokenType.COMMA)
            case '.': self.__add_token(TokenType.DOT)
            case '-': self.__add_token(TokenType.MINUS)
            case '+': self.__add_token(TokenType.PLUS)
            case ';': self.__add_token(TokenType.SEMICOLON)
            case '*': self.__add_token(TokenType.STAR)
            case '!': self.__add_token(TokenType.BANG_EQUAL if self.__match('=') else TokenType.BANG)
            case '=': self.__add_token(TokenType.EQUAL_EQUAL if self.__match('=') else TokenType.EQUAL)
            case '<': self.__add_token(TokenType.LESS_EQUAL if self.__match('=') else TokenType.LESS)
            case '>': self.__add_token(TokenType.GREATER_EQUAL if self.__match('=') else TokenType.GREATER)
            case '/':
                if (self.__match('/')):
                    while (self.__peek() != '\n' and not self.__is_at_end()):
                        self.__advance()
                else:
                    self.__add_token(TokenType.SLASH)
            case '"':
                self.__string()
            case default:
                if default.isalpha():
                    self.__identifier()
                elif default.isdigit():
                    self.__number()
                elif not default.isspace():
                    print(f"Error====>{default}<========")
                    Surnix.error(Scanner.line, "Unexpected character.")
