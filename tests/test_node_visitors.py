
from source.context.translators import LISPTranslator, RPNTranslator
from source.syntax.parser import Parser
from source.tokenization.lexer import Lexer


def test_RPN_translator_success():
    lexer = Lexer("(5 + 3) * 12 / 3")

    parser = Parser(lexer)

    translator = RPNTranslator(parser)
    translator()
    assert translator.stack == ""


def test_lisp_translator_success():
    lexer = Lexer("(5 + 3) * 12 / 3")

    parser = Parser(lexer)

    lisp_translator = LISPTranslator(parser)
    lisp_translator()
    assert "" == "".join(lisp_translator.stack)  # correct result,(+ 2 (* 3 5)).
