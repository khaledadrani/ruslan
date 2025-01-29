from abc import ABC, abstractmethod
from source.tokenization.tokens import Token


class TokenHandler(ABC):
    def __init__(self, text: str, pos: int):
        self.text = text
        self.pos = pos

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

    @abstractmethod
    def __call__(self) -> Token:
        """
        This method will be implemented by each specific handler.
        It should process the current state of the lexer and return a token,
        or return None if it cannot handle the current state.
        """
        pass
