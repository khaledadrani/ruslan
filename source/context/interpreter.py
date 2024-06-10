from source.context.node_visitors import NodeVisitor
from source.tokenization.tokens import TokenType


class Interpreter(NodeVisitor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.GLOBAL_SCOPE = {}

    def visit_BinOpNode(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == TokenType.DOUBLE_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == TokenType.PERCENT:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == TokenType.ASSIGN:
            self.memory[node.left.value] = self.visit(node.right)
            return str(node.left.value)

        raise ValueError("Unknown Bin OP Node!", node)

    def visit_NumNode(self, node):
        return int(node.value)

    def visit_UnaryOpNode(self, node):
        return - self.visit(node.right)

    def visit_CompoundNode(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_AssignNode(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_IDNode(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val
