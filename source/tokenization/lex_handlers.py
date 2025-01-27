from abc import ABC, abstractmethod

from source.tokenization.lexer import Lexer
from source.tokenization.tokens import TokenType, Token, RESERVED_KEYWORDS


class TokenHandler(ABC):
    def __init__(self, lexer: 'Lexer'):
        self.lexer = lexer

    @abstractmethod
    def __call__(self) -> None:
        """
        This method will be implemented by each specific handler.
        It should process the current state of the lexer and return a token,
        or return None if it cannot handle the current state.
        """
        pass


class DummyTokenHandler(TokenHandler):
    def __call__(self) -> str:
        # TODO need fixing
        token = self.lexer.current_char
        return token


class WhitespaceHandler(TokenHandler):

    def skip_whitespace(self):
        lexer = self.lexer
        while lexer.pos is not None and lexer.current_char.isspace():
            lexer.advance()

    def __call__(self) -> None:
        # Handle whitespace logic here
        if self.lexer.current_char.isspace():
            self.skip_whitespace()


class ParenthesisHandler(TokenHandler):

    def __call__(self):
        if self.lexer.current_char == '(':
            self.lexer.advance()
            return Token(TokenType.LEFT_PARA, "(")

        if self.lexer.current_char == ')':
            self.lexer.advance()
            return Token(TokenType.RIGHT_PARA, ")")


class OperatorHandler(TokenHandler):

    def get_div(self):
        lexer = self.lexer
        lexer.advance()
        if lexer.current_char == '/':
            lexer.advance()
            return Token(TokenType.DOUBLE_DIV, '//')
        else:
            lexer.advance()
            return Token(TokenType.DIV, '/')

    def __call__(self):
        if self.lexer.current_char == '+':
            self.lexer.advance()
            return Token(TokenType.PLUS, '+')

        if self.lexer.current_char == '-':
            self.lexer.advance()
            return Token(TokenType.MINUS, '-')

        if self.lexer.current_char == '*':
            self.lexer.advance()
            return Token(TokenType.MUL, '*')

        if self.lexer.current_char == '/':
            return self.get_div()

        if self.lexer.current_char == "%":
            self.lexer.advance()
            return Token(TokenType.PERCENT, "%")


class IntegerHandler(TokenHandler):

    def get_integer(self):
        """Return a (multidigit) integer consumed from the input."""
        lexer = self.lexer
        result = ''
        while lexer.pos is not None and lexer.current_char.isdigit():
            result += lexer.current_char
            lexer.advance()

        if not result:
            raise ValueError("Not a correct integer token")

        return result

    def __call__(self):
        if self.lexer.current_char.isdigit():
            return Token(TokenType.INTEGER, self.get_integer())


class IdentifierHandler(TokenHandler):

    def get_id(self) -> Token:
        """Handle identifiers and reserved keywords"""
        lexer = self.lexer
        result = ''
        while lexer.pos is not None and lexer.current_char.isalnum():
            result += lexer.current_char
            lexer.advance()
        return RESERVED_KEYWORDS.get(result, Token(TokenType.ID, result))

    def __call__(self):
        if self.lexer.current_char.isalpha():
            return self.get_id()


class NewTokenHandler(TokenHandler):

    def __call__(self):
        if self.lexer.current_char == ':':
            if self.lexer.peek() == '=':
                self.lexer.advance()
                self.lexer.advance()
                return Token(TokenType.ASSIGN, ':=')

        if self.lexer.current_char == ';':
            self.lexer.advance()
            return Token(TokenType.SEMI, ';')

        if self.lexer.current_char == '.':
            self.lexer.advance()
            return Token(TokenType.DOT, '.')



