from source.tokenization.lexer import PascalLexer
from source.tokenization.lexer import Lexer
from source.tokenization.tokens import TokenType, Token


def test_advance_success():
    lexer = PascalLexer("3 * 5")
    token = next(lexer)
    assert token.value == "3"
    token = next(lexer)
    assert token.value == " "
    token = next(lexer)
    assert token.value == "*"
    token = next(lexer)
    assert token.value == " "
    token = next(lexer)
    assert token.value == "5"

    try:
        next(lexer)  # This should raise StopIteration
    except StopIteration as error:
        # Ensure that StopIteration was raised, and we don't expect a token after that
        assert True  # This assertion will confirm that the exception was raised
        return  # Exit the function since we expect StopIteration here

        # If we get here, the StopIteration exception was not raised
    assert False, "Expected StopIteration, but it was not raised."
