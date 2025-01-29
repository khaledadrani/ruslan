from typing import List, Type

from source.tokenization.token_handlers.base_token_handler import TokenHandler
from source.tokenization.token_handlers.common_token_handlers import WhitespaceHandler, ParenthesisHandler, \
    OperatorHandler, IntegerHandler, IdentifierHandler, NewTokenHandler
from source.tokenization.tokens import Token, TokenType


class Lexer:
    def __init__(self, text: str, handlers: List[Type[TokenHandler]]):
        self.text = text
        self.pos = 0

        self.handlers = handlers

    def get_next_token(self, text, pos) -> Token:
        #while self.pos is not None:
        if pos is None or pos >= len(text):
            return Token(TokenType.EOF, None, len(text))

        for handler in self.handlers:
            handler_instance = handler(text, pos)
            token = handler_instance()
            if token:
                return token
        raise TypeError(f"Unknown Token Type  `{text[pos]}`")

        #return Token(TokenType.EOF, None, text[pos])

    def __iter__(self):
        return self

    def __next__(self):
        # if self.pos is None or self.pos >= len(self.text):
        #     raise StopIteration

        token = self.get_next_token(self.text, self.pos)
        if token.type == TokenType.EOF:
            raise StopIteration

        self.pos = token.pos
        return token


class PascalLexer(Lexer):
    def __init__(self, text: str):
        handlers = [WhitespaceHandler, ParenthesisHandler, OperatorHandler,
                    IntegerHandler, IdentifierHandler, NewTokenHandler]

        super().__init__(text=text, handlers=handlers)
