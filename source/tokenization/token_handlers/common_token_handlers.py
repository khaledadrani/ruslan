from source.tokenization.token_handlers.base_token_handler import TokenHandler
from source.tokenization.tokens import TokenType, Token, RESERVED_KEYWORDS


class WhitespaceHandler(TokenHandler):

    def skip_whitespace(self):
        result = ""
        while self.pos is not None and self.current_char.isspace():
            result += self.current_char
            self.advance()

        return result

    def __call__(self) -> Token:
        # Handle whitespace logic here
        if self.current_char.isspace():
            return Token(TokenType.WHITESPACE, self.skip_whitespace(), self.pos)


class ParenthesisHandler(TokenHandler):

    def __call__(self) -> Token:
        if self.current_char == '(':
            self.advance()
            return Token(TokenType.LEFT_PARA, "(", self.pos)

        if self.current_char == ')':
            self.advance()
            return Token(TokenType.RIGHT_PARA, ")", self.pos)


class OperatorHandler(TokenHandler):

    def get_div(self):
        self.advance()
        if self.current_char == '/':
            self.advance()
            return Token(TokenType.DOUBLE_DIV, '//', self.pos)
        else:
            self.advance()
            return Token(TokenType.DIV, '/', self.pos)

    def __call__(self):
        if self.current_char == '+':
            self.advance()
            return Token(TokenType.PLUS, '+', self.pos)

        if self.current_char == '-':
            self.advance()
            return Token(TokenType.MINUS, '-', self.pos)

        if self.current_char == '*':
            self.advance()
            return Token(TokenType.MUL, '*', self.pos)

        if self.current_char == '/':
            return self.get_div()

        if self.current_char == "%":
            self.advance()
            return Token(TokenType.PERCENT, "%", self.pos)


class IntegerHandler(TokenHandler):

    def get_integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.pos is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if not result:
            raise ValueError("Not a correct integer token")

        return result

    def __call__(self):
        if self.current_char.isdigit():
            return Token(TokenType.INTEGER, self.get_integer(), self.pos)


class IdentifierHandler(TokenHandler):

    def get_id(self) -> Token:
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.pos is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        id_token_callable = RESERVED_KEYWORDS.get(result, lambda pos: Token(TokenType.ID, result, pos))
        return id_token_callable(self.pos)

    def __call__(self):
        if self.current_char.isalpha():
            return self.get_id()


class NewTokenHandler(TokenHandler):

    def __call__(self):
        if self.current_char == ':':
            if self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.ASSIGN, ':=', self.pos)

        if self.current_char == ';':
            self.advance()
            return Token(TokenType.SEMI, ';', self.pos)

        if self.current_char == '.':
            self.advance()
            return Token(TokenType.DOT, '.', self.pos)
