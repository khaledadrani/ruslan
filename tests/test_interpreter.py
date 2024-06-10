from source.context.interpreter import Interpreter
from source.syntax.parser import Parser
from source.tokenization.lexer import Lexer


def test_basic_intepreter():

    program = """
    BEGIN
        BEGIN
            number := 2;
            a := number;
            b := 10 * a + 10 * number / 4;
            c := a - - b
        END;
        x := 11;
    END.
    """
    lexer = Lexer(program)

    parser = Parser(lexer)

    interpreter = Interpreter(parser)

    interpreter(), 5 + 3 - 2 * (7 + 3)
