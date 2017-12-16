import unittest
import os
import sys

from architecture.code_tree import CodeTree, TreeNode
from architecture.documentation4fragments import Documentation4Fragmnets
from architecture.fragments import Fragment

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from architecture import fragments

class TestDocumentation4Fragments(unittest.TestCase):

    def test_empty_documentation_when_tree_is_empty(self):
        code_lines = []
        filename = 'kek'
        tree = CodeTree(code_lines)
        docs_nodes = Documentation4Fragmnets(tree, code_lines, filename).get_documentation_nodes()
        self.assertEqual(len(docs_nodes), 0)

    def test_correct_documentation_when_tree_contains_one_element(self):
        code_lines = ['def main():', '    pass']
        fragment = Fragment(0, 1, 'def', 0)
        tree = CodeTree(code_lines)
        tree.add_fragment(fragment)
        self.assertTrue(tree.get_root() == TreeNode(fragment))

    # def test_correct_documentation_when_tree_is_empty(self):
    #     code_lines = []
    #     tree = CodeTree(code_lines)
    #     self.assertTrue(tree.get_root() == TreeNode(Fragment(0, 0, 'file', 0)))

    def get_tree_node(self, first_line: int, last_line: int, type_fragment: str, nesting: int):
        fragment = Fragment(first_line, last_line, type_fragment, nesting)
        return TreeNode(fragment)


if __name__ == "__main__":
    unittest.main()