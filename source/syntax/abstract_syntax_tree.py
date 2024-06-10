from typing import List, Optional, Any

from source.tokenization.tokens import Token


class ASTNode:
    def __init__(self, value: Any = None, children: Optional[List["ASTNode"]] = None):
        self.value = value
        self.children = children


class BinOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: Token, right: ASTNode):
        super().__init__(value=op.value, children=[left, right])
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOpNode(({self.left.value})~({self.token.value})~({self.right.value}))"

    def __str__(self):
        return self.__repr__()


class CompoundNode(ASTNode):
    """Represents a 'BEGIN ... END' block"""

    def __init__(self):
        super().__init__(children=[])


class AssignNode(BinOpNode):
    ...


class NumNode(ASTNode):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NumNode({self.value})"

    def __str__(self):
        return self.__repr__()


class IDNode(ASTNode):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"IDNode({self.value})"

    def __str__(self):
        return self.__repr__()


class NoOp(ASTNode):
    pass


class UnaryOpNode(ASTNode):
    def __init__(self, op: Token, right: ASTNode):
        super().__init__(value=op.value, children=[right])
        self.right = right
        self.token = self.op = op

    def __repr__(self):
        return f"UnaryOpNode(({self.token.value})~({self.right.value}))"

    def __str__(self):
        return self.__repr__()
