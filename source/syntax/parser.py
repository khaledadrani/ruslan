from functools import partial
from typing import Union

from source.syntax.abstract_syntax_tree import NumNode, UnaryOpNode, IDNode, BinOpNode, CompoundNode, NoOp, AssignNode
from source.tokenization.tokens import TokenType


class Parser:
    """
    program : compound_statement DOT

    compound_statement : BEGIN statement_list END

    statement_list : statement
                   | statement SEMI statement_list

    statement : compound_statement
              | assignment_statement
              | empty

    assignment_statement : variable ASSIGN expr

    empty :

    expr: term ((PLUS | MINUS) term)*

    term: factor ((MUL | DIV) factor)*

    factor : PLUS factor
           | MINUS factor
           | INTEGER
           | LPAREN expr RPAREN
           | variable

    variable: ID
    """

    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        # print(self.current_token, token_type)
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Expected to eat {token_type} got {self.current_token.type}")

    def parse_factor(self) -> Union[NumNode, IDNode, BinOpNode, UnaryOpNode]:
        """factor : PLUS factor
           | MINUS factor
           | INTEGER
           | LPAREN expr RPAREN
           | variable
        """
        token = self.current_token

        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            return UnaryOpNode(token, self.parse_factor())

        if token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnaryOpNode(token, self.parse_factor())

        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return NumNode(token)

        if token.type == TokenType.ID:
            self.eat(TokenType.ID)
            return IDNode(token)

        else:
            self.eat(TokenType.LEFT_PARA)
            node = self.parse_expr()
            self.eat(TokenType.RIGHT_PARA)
            return node

    def parse_term(self) -> BinOpNode:
        """term : factor ((MUL | DIV | DOUBLE_DIV | PERCENT ) factor)*"""
        node = self.parse_factor()

        while self.current_token.type in (TokenType.MUL,
                                          TokenType.DIV,
                                          TokenType.DOUBLE_DIV,
                                          TokenType.PERCENT):
            token = self.current_token

            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)

            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)

            elif token.type == TokenType.DOUBLE_DIV:
                self.eat(TokenType.DOUBLE_DIV)

            elif token.type == TokenType.PERCENT:
                self.eat(TokenType.PERCENT)

            else:
                raise Exception("Bad Token Type in parse_term")

            node = BinOpNode(left=node, op=token, right=self.parse_factor())

        return node

    def parse_expr(self):
        """
        expr: term ((PLUS|MINUS) term)*
        """

        node = self.parse_term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)

            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            else:
                raise Exception("Bad Token Type in parse expr")

            node = BinOpNode(left=node, op=token, right=self.parse_term())

        return node

    @staticmethod
    def parse_empty() -> NoOp:
        """An empty production"""
        return NoOp()

    def parse_variable(self) -> IDNode:
        node = IDNode(self.current_token)
        self.eat(TokenType.ID)
        return node

    def parse_assignment_statement(self):
        """
            assignment_statement : variable ASSIGN expr
            """
        left = self.parse_variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.parse_expr()
        node = AssignNode(left, token, right)
        return node

    def parse_compound_statement(self):
        """
        compound_statement: BEGIN statement_list END
        """
        self.eat(TokenType.BEGIN)
        nodes = self.parse_statement_list()
        self.eat(TokenType.END)

        root = CompoundNode()
        for node in nodes:
            root.children.append(node)

        return root

    def parse_statement(self):

        if self.current_token.type == TokenType.BEGIN:
            node = self.parse_compound_statement()
        elif self.current_token.type == TokenType.ID:
            node = self.parse_assignment_statement()
        else:
            node = self.parse_empty()
        return node

    def parse_statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.parse_statement()

        results = [node]

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.parse_statement())

        if self.current_token.type == TokenType.ID:
            raise TypeError(f"Not ID in parse_statement_list {self.current_token.type}")

        return results

    def parse_program(self):
        """program : compound_statement DOT"""
        node = self.parse_compound_statement()
        self.eat(TokenType.DOT)
        return node

    def parse(self):
        node = self.parse_program()

        if self.current_token.type != TokenType.EOF:
            raise ValueError("Program not ending with EOF")

        return node
