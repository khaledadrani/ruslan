from source.syntax.parser import Parser


class NodeVisitor:
  def __init__(self, parser: Parser):
        self.parser = parser

  def visit(self, node):
      method_name = 'visit_' + type(node).__name__
      visitor = getattr(self, method_name, self.generic_visit)
      return visitor(node)

  def generic_visit(self, node):
      raise Exception('No visit_{} method'.format(type(node).__name__))

  def __call__(self):
      tree = self.parser.parse()
      return self.visit(tree)





