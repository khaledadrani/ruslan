from source.tokenization.lex_handlers import WhitespaceHandler, ParenthesisHandler, OperatorHandler, IntegerHandler, \
    IdentifierHandler, NewTokenHandler
from source.tokenization.lexer import Lexer


class PascalLexer(Lexer):
    def __init__(self, text: str):
        handlers = [WhitespaceHandler, ParenthesisHandler, OperatorHandler,
                    IntegerHandler, IdentifierHandler, NewTokenHandler]

        super().__init__(text=text, handlers=handlers)
