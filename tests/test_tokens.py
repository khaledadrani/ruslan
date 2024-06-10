from source.syntax.abstract_syntax_tree import BinOpNode, NumNode, UnaryOpNode
from source.tokenization.tokens import TokenType, Token


def test_simple_token():
    assert 'INTEGER' == TokenType.INTEGER


def test_init_token_integer_success():
    token = Token(TokenType.INTEGER, 10)
    assert token.type == TokenType.INTEGER
    assert token.value == 10
    assert token.__repr__() == "Token(INTEGER, 10)"


def test_parse_bin_op_node_success():
    mul_token = Token(TokenType.MUL, '*')
    plus_token = Token(TokenType.PLUS, '+')
    mul_node = BinOpNode(
        left=NumNode(Token(TokenType.INTEGER, "1")),
        op=plus_token,
        right=NumNode(Token(TokenType.INTEGER, "213"))
    )

    assert str(mul_node) == "BinOpNode((1)~(+)~(213))"


def test_parse_unary_op_node():
    res = UnaryOpNode(op= Token(TokenType.MINUS, '-'),
                      right=NumNode(Token(TokenType.INTEGER, "213")))

    assert str(res) == "UnaryOpNode((-)~(213))"
