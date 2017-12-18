import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from architecture import code_tree
from architecture import fragments

class TestCodeTree(unittest.TestCase):
    def test_correctTree_whenThereAreNoCodeFragments(self):
        code_lines = []
        nodes = self.get_nodes(code_lines)
        self.assertTrue(nodes == [])

    def test_correctTree_whenThereAreNoCodeFragments2(self):
        code_lines = ['oh my code']
        nodes = self.get_nodes(code_lines)
        self.assertTrue(nodes == [])

    def test_correctTree_wheThereAreNoCodeFragments3(self):
        code_lines = ['']
        nodes = self.get_nodes(code_lines)
        self.assertTrue(nodes == [])


    def test_correctTree_whenThereAreNoCodeFragments4(self):
        code_lines = [
            'oh my code',
            ''
            'oh my code'
        ]
        nodes = self.get_nodes(code_lines)
        self.assertTrue(nodes == [])

    def test_correctTree_whenOneCodeFragments(self):
        code_lines = ['class kek:']
        expected = [
            code_tree.TreeNode(
                fragments.Fragment(0, 0, 'class', 0)
            )
        ]
        actual = self.get_nodes(code_lines)
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertTrue(i in actual)

    def test_correctTree_whenFewNestedCodeFragments(self):
        code_lines = ['class kek:', '    def cheburek:', '        pass']
        expected = [
            code_tree.TreeNode(
                fragments.Fragment(0, 2, 'class', 0),
                [code_tree.TreeNode(fragments.Fragment(1, 2, 'def', 4))]
            ),
            code_tree.TreeNode(
                fragments.Fragment(1, 2, 'def', 4)
            )
        ]
        actual = self.get_nodes(code_lines)
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertTrue(i in actual)

    def test_correctTree_whenFewNotNestedCodeFragments(self):
        code_lines = ['class kek:', '    pass', 'def cheburek:', '    pass']
        expected = [
            code_tree.TreeNode(
                fragments.Fragment(0, 1, 'class', 0)
            ),
            code_tree.TreeNode(
                fragments.Fragment(2, 3, 'def', 0)
            )
        ]
        actual = self.get_nodes(code_lines)
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertTrue(i in actual)

    def get_nodes(self, code_lines):
        tree = code_tree.CodeTree(code_lines)
        result = tree.get_root().nested_nodes
        for i in tree.get_root().nested_nodes:
            if i.nested_nodes != None:
                result += i.nested_nodes
        return result

if __name__ == "__main__":
    unittest.main()