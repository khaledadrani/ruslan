from source.tokenization.lexer import Lexer
from source.tokenization.tokens import TokenType, Token


def test_advance_success():
  lexer = Lexer("3 * 5")
  assert lexer.current_char == "3"
  lexer.advance()
  assert lexer.current_char == " "
  lexer.advance()
  assert lexer.current_char == "*"
  lexer.advance()
  assert lexer.current_char == " "
  lexer.advance()
  assert lexer.current_char == "5"

def test_lex_integer_failure_not_correct_integer():
  lexer = Lexer("3 * 5")
  lexer.get_integer()
  assert lexer.current_char
  try:
    lexer.get_integer()
  except ValueError as error:
    assert str(error) == "Not a correct integer token"


def test_get_next_token_success():
  tokens = [Token(TokenType.INTEGER, '3'),
      Token(TokenType.MUL, '*'),
      Token(TokenType.INTEGER, '5'),
      Token(TokenType.EOF, None),
      Token(TokenType.EOF, None),
      Token(TokenType.EOF, None),
      Token(TokenType.EOF, None)
      ]

  lexer = Lexer("3 * 5")

  for index in range(7):
    assert lexer.get_next_token() == tokens[index]

def test_double_div_percent():

  lexer = Lexer("3 // 5 + 10 % 2 / 2")

  tokens = [
      Token(TokenType.INTEGER, '3'),
      Token(TokenType.DOUBLE_DIV, '//'),
      Token(TokenType.INTEGER, '5'),
      Token(TokenType.PLUS, '+'),
      Token(TokenType.INTEGER, '10'),
      Token(TokenType.PERCENT, '%'),
      Token(TokenType.INTEGER, '2'),
      Token(TokenType.DIV, '/'),
      Token(TokenType.INTEGER, '2')
  ]

  for index in range(9):
    assert lexer.get_next_token() == tokens[index]