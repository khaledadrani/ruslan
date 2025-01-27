from typing import TYPE_CHECKING, List, Type

if TYPE_CHECKING:
    from source.tokenization.lex_handlers import TokenHandler

from source.tokenization.tokens import Token, TokenType


class Lexer:
    def __init__(self, text: str, handlers: List[Type["TokenHandler"]]):
        self.text = text
        self.pos = 0

        self.handlers = [handler(lexer=self) for handler in handlers]

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

    def get_next_token(self):
        while self.pos is not None:
            for handler in self.handlers:
                token = handler()
                if token:
                    return token
            raise TypeError(f"Unknown Token Type  `{self.current_char}`")

        return Token(TokenType.EOF, None)




