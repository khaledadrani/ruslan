from source.context.node_visitors import NodeVisitor


class LISPTranslator(NodeVisitor):
    """
  prints it out in postfix notation, also known as Reverse Polish Notation (RPN)
  """

    def __init__(self, parser):
        super().__init__(parser)
        self.stack = []

    def visit_BinOpNode(self, node):
        self.stack.append("(")
        self.stack.append(node.op.value)
        self.visit(node.left)
        self.visit(node.right)
        self.stack.append(")")

    def visit_NumNode(self, node):
        self.stack.append(node.value)


class RPNTranslator(NodeVisitor):
    """
  prints it out in postfix notation, also known as Reverse Polish Notation (RPN)
  """

    def __init__(self, parser):
        super().__init__(parser)
        self.stack = []

    def visit_BinOpNode(self, node):
        self.visit(node.left)
        self.visit(node.right)
        self.stack.append(node.op.value)

    def visit_NumNode(self, node):
        self.stack.append(node.value)
