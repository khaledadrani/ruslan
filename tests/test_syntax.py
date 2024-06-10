from source.syntax.abstract_syntax_tree import ASTNode, BinOpNode
from source.tokenization.tokens import Token, TokenType


def test_ast_node_init():
  left = ASTNode(value="1")
  right = ASTNode(value="2")
  main = ASTNode(value="+", children=[left, right])

  assert main.value == "+" and main.children == [left, right]


def test_bin_op_node_init():
  left = ASTNode(value="1")
  right = ASTNode(value="2")
  main = BinOpNode(op=Token(TokenType.MUL, "+"), left=left, right=right)

  assert main.value == "+" and main.children == [left, right]
  assert main.token == Token(type=TokenType.MUL, value="+")
  assert main.left == left
  assert main.right == right