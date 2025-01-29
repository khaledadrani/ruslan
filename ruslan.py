from source.tokenization.lexer import PascalLexer

lexer = PascalLexer("10 + 5 * 2 / (10-2)")

for token in lexer:
    print(token)
