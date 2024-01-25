from TokenType import TokenType
from Binary import Binary
from Unary import Unary
from Literal import Literal
from Print import Print
from Expression import Expression
from Var import Var
from Variable import Variable
from Block import Block
from Assign import Assign


class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.current = 0

    def __equality(self):
        expr = self.__comparison()
        while (self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            operator = self.__previous()
            right = self.__comparison()
            expr = Binary(expr, operator, right)

        return expr

    def __peek(self):
        return self.tokens[self.current]

    def __previous(self):
        return self.tokens[self.current-1]

    def __advance(self):
        if not self.__isAtEnd():
            self.current += 1
        return self.__previous()

    def __isAtEnd(self):
        return self.__peek().type == TokenType.EOF

    def __check(self, type):
        if self.__isAtEnd():
            return False
        return self.__peek().type == type

    def __match(self, *tokenTypes):
        for type in tokenTypes:
            if self.__check(type):
                self.__advance()
                return True
        return False

    def __comparison(self):
        expr = self.__term()
        while (self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)):
            operator = self.__previous()
            right = self.__term()
            expr = Binary(expr, operator, right)

        return expr

    def __term(self):
        expr = self.__factor()
        while (self.__match(TokenType.MINUS, TokenType.PLUS)):
            operator = self.__previous()
            right = self.__factor()
            expr = Binary(expr, operator, right)
        return expr

    def __factor(self):
        expr = self.__unary()
        while (self.__match(TokenType.SLASH, TokenType.STAR)):
            operator = self.__previous()
            right = self.__unary()
            expr = Binary(expr, operator, right)
        return expr

    def __unary(self):
        if (self.__match(TokenType.BANG, TokenType.MINUS)):
            operator = self.__previous()
            right = self.__unary()
            return Unary(operator, right)

        return self.__primary()

    def __consume(self, type, message):
        if (self.__check(type)):
            return self.__advance()
        self.__error(self.__peek(), message)

    def __error(self, token, message):
        from Surnix import Surnix
        Surnix.error_token(token, message)
        return Exception(message)

    def __synchronize(self):
        self.__advance()

        while (not self.__isAtEnd()):
            if (self.__previous().type == TokenType.SEMICOLON):
                return

            match(self.__peek().type):
                case TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN:
                    return

            self.__advance()

    def __block(self):
        statements = list()
        while (not self.__check(TokenType.RIGHT_BRACE) and not self.__isAtEnd()):
            statements.append(self.__declaration())
        self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def __primary(self):
        if (self.__match(TokenType.FALSE)):
            return Literal(False)
        if (self.__match(TokenType.TRUE)):
            return Literal(True)
        if (self.__match(TokenType.NIL)):
            return Literal(None)
        if (self.__match(TokenType.NUMBER, TokenType.STRING)):
            return Literal(self.__previous().literal)
        if (self.__match(TokenType.LEFT_PAREN)):
            expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN,
                           "Expect ')' after expression.")
            return expr
        if (self.__match(TokenType.IDENTIFIER)):
            return Variable(self.__previous())
        raise self.__error(self.__peek(), "Expect expression.")

    def __assignment(self):
        expr = self.__equality()

        if (self.__match(TokenType.EQUAL)):
            equals = self.__previous()
            value = self.__assignment()
            if (isinstance(expr, Variable)):
                name = expr.name
                return Assign(name, value)

            self.__error(equals, "Invalid assignment target.")

        return expr

    def __expression(self):
        return self.__assignment()

    def __printStatement(self):
        value = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Print(value)

    def __expressionStatement(self):
        value = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Expression(value)

    def __statement(self):
        if (self.__match(TokenType.PRINT)):
            return self.__printStatement()
        if (self.__match(TokenType.LEFT_BRACE)):
            return Block(self.__block())
        return self.__expressionStatement()

    def __varDeclaration(self):
        name = self.__consume(TokenType.IDENTIFIER, "Expect Variable Name")
        initializer = None
        if (self.__match(TokenType.EQUAL)):
            initializer = self.__expression()

        self.__consume(TokenType.SEMICOLON,
                       "Expect ';' after variable declaration")

        return Var(name, initializer)

    def __declaration(self):
        try:
            if (self.__match(TokenType.VAR)):
                return self.__varDeclaration()
            return self.__statement()
        except:
            self.__synchronize()
            return None

    def parse(self):
        statements = []
        while (not self.__isAtEnd()):
            statements.append(self.__declaration())

        return statements
