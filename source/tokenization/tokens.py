from enum import Enum
from typing import Any


class TokenType(str, Enum):
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    EOF = 'EOF'
    LEFT_PARA = 'LEFT_PARA'
    RIGHT_PARA = 'RIGHT_PARA'
    PERCENT = 'PERCENT'
    DOUBLE_DIV = 'DOUBLE_DIV'
    ID = 'ID'
    ASSIGN = 'ASSIGN'
    BEGIN = 'BEGIN'
    END = 'END'
    SEMI = "SEMI"
    DOT = "DOT"

    def __str__(self):
        return self.value


class Token(object):
    def __init__(self, type: TokenType, value: Any):
        # token type: INTEGER, PLUS, MINUS, MUL, DIV, or EOF
        self.type = type
        # token value: non-negative integer value, '+', '-', '*', '/', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value


RESERVED_KEYWORDS = {
    'BEGIN': Token(TokenType.BEGIN, TokenType.BEGIN),
    'END': Token(TokenType.BEGIN, TokenType.END),
}
