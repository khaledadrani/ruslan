from source.tokenization.tokens import Token, TokenType, RESERVED_KEYWORDS


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    @property
    def current_char(self):
        return self.text[self.pos]

    def peek(self):
        """
        return the next token after the current position without
        incrementing the self.pos cursor
        """
        return self.text[self.pos + 1] if self.pos else None

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.pos = None

    def skip_whitespace(self):
        while self.pos is not None and self.current_char.isspace():
            self.advance()

    def get_div(self):
        self.advance()
        if self.current_char == '/':
            self.advance()
            return Token(TokenType.DOUBLE_DIV, '//')
        else:
            self.advance()
            return Token(TokenType.DIV, '/')

    def get_integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.pos is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if not result:
            raise ValueError("Not a correct integer token")

        return result

    def get_id(self) -> Token:
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.pos is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return RESERVED_KEYWORDS.get(result, Token(TokenType.ID, result))

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

    This method is responsible for breaking a sentence
    apart into tokens. One token at a time.
    """

        while self.pos is not None:

            if self.current_char.isspace():  # condition,action, return
                self.skip_whitespace()
                continue

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LEFT_PARA, "(")

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RIGHT_PARA, ")")

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MUL, '*')

            if self.current_char == '/':
                return self.get_div()

            if self.current_char == "%":
                self.advance()
                return Token(TokenType.PERCENT, "%")

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.get_integer())

            if self.current_char.isalpha():
                return self.get_id()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.ASSIGN, ':=')

            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMI, ';')

            if self.current_char == '.':
                self.advance()
                return Token(TokenType.DOT, '.')

            raise TypeError(f"Unknown Token Type  `{self.current_char}`")

        return Token(TokenType.EOF, None)
