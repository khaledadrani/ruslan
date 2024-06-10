from typing import List
import argparse
import textwrap
from PIL import Image
from IPython.display import display
from source.syntax.abstract_syntax_tree import ASTNode


def search_breadth_first(node: ASTNode) -> List[ASTNode]:
    visited = []
    queue = [node]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            # print(node, end=' ')
            visited.append(node)
            if node.children:
                queue.extend(node.children)

    return visited


import textwrap


class ParseTreeVisualizer:
    def __init__(self, parser):
        self.parser = parser
        self.ncount = 1
        self.dot_header = [textwrap.dedent("""\
        digraph astgraph {
          node [shape=none, fontsize=12, fontname="Courier", height=.1];
          ranksep=.3;
          edge [arrowsize=.5]

        """)]
        self.dot_body = []
        self.dot_footer = ['}']

    def bfs(self, node):
        ncount = 1
        queue = []
        queue.append(node)
        s = '  node{} [label="{}"]\n'.format(ncount, node.value)
        self.dot_body.append(s)
        node._num = ncount
        ncount += 1

        while queue:
            node = queue.pop(0)
            if node.children:
                for child_node in node.children:
                    s = '  node{} [label="{}"]\n'.format(ncount, child_node.value)
                    self.dot_body.append(s)
                    child_node._num = ncount
                    ncount += 1
                    s = '  node{} -> node{}\n'.format(node._num, child_node._num)
                    self.dot_body.append(s)
                    queue.append(child_node)

    def gendot(self):
        tree = self.parser.parse()
        self.bfs(tree)
        return ''.join(self.dot_header + self.dot_body + self.dot_footer)

    # def show_colab(self):
    #     """
    #     Run this in Colab
    #     :return:
    #     """
    #     from PIL import Image
    #     from IPython.display import display
    #     content = self.gendot()
    #     with open("parsetree.dot", "w") as f:
    #       f.write(content)
    #
    #     !dot -Tpng -o parsetree.png parsetree.dot
    #
    #     with Image.open("parsetree.png") as image:
    #       # Display the image
    #       image.show()
    #
    #
    #       display(image)
