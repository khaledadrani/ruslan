from source.syntax.parser import Parser
from source.syntax.utils import search_breadth_first
from source.tokenization.lexer import Lexer
from source.tokenization.tokens import TokenType, Token


def test_basic_parser_success():
    lexer = Lexer("3 * 5")

    parser = Parser(lexer)
    assert Token(TokenType.INTEGER, '3') == parser.current_token
    parser.eat(TokenType.INTEGER)
    assert Token(TokenType.MUL, '*') == parser.current_token
    parser.eat(TokenType.MUL)


def test_parse_factor_success():
    lexer = Lexer("3 * 5")

    parser = Parser(lexer)

    assert "3" == parser.parse_factor().value
    parser.eat("MUL")
    assert "5" == parser.parse_factor().value


def test_parse_term_mul_div_success():
    expected = ["BinOpNode((/)~(*)~(5))", "BinOpNode((3)~(/)~(5))", "NumNode(5)", "NumNode(3)", "NumNode(5)"]

    lexer = Lexer("3 / 5 * 5")

    parser = Parser(lexer)

    root = parser.parse_term()

    assert str(root) == "BinOpNode((/)~(*)~(5))"
    assert [str(node) for node in search_breadth_first(root)] == expected


def test_parse_expr_plus_minus_success():
    expected = ["BinOpNode((+)~(+)~(1000))",
                "BinOpNode((/)~(+)~(3))",
                "NumNode(1000)",
                "BinOpNode((10)~(/)~(2))",
                "NumNode(3)",
                "NumNode(10)",
                "NumNode(2)"
                ]
    lexer = Lexer("10 / 2 + 3 + 1000")

    parser = Parser(lexer)
    # parser.parse_expr()
    root = parser.parse_expr()
    assert expected == [str(node) for node in search_breadth_first(root)]


def test_parse_expr_double_div_success():
    expected = ["BinOpNode((//)~(+)~(*))",
                "BinOpNode((10)~(//)~(2))",
                "BinOpNode((3)~(*)~(1))",
                "NumNode(10)",
                "NumNode(2)",
                "NumNode(3)",
                "NumNode(1)"]
    lexer = Lexer("10 // 2 + 3 * 1")

    parser = Parser(lexer)
    root = parser.parse_expr()
    assert expected == [str(node) for node in search_breadth_first(root)]


def test_para():
    expected = ["BinOpNode((5)~(+)~(/))",
                "NumNode(5)",
                "BinOpNode((10)~(/)~(+))",
                "NumNode(10)",
                "BinOpNode((2)~(+)~(3))",
                "NumNode(2)",
                "NumNode(3)"
                ]

    lexer = Lexer("5 + (10 /  (2 + 3) )")

    parser = Parser(lexer)

    root = parser.parse_expr()
    assert expected == [str(node) for node in search_breadth_first(root)]


def test_more_difficult_case():
    expected = ["BinOpNode((7)~(+)~(*))",
                "NumNode(7)",
                "BinOpNode((3)~(*)~(/))",
                "NumNode(3)",
                "BinOpNode((10)~(/)~(-))",
                "NumNode(10)",
                "BinOpNode((/)~(-)~(1))",
                "BinOpNode((12)~(/)~(+))",
                "NumNode(1)",
                "NumNode(12)",
                "BinOpNode((3)~(+)~(1))",
                "NumNode(3)",
                "NumNode(1)"
                ]
    lexer = Lexer("7 + 3 * (10 / (12 / (3 + 1) - 1))")

    parser = Parser(lexer)

    root = parser.parse_expr()
    assert expected == [str(node) for node in search_breadth_first(root)]
