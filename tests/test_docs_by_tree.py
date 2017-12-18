import unittest
import os
import sys

from architecture.code_tree import CodeTree, TreeNode
from architecture.docs_by_tree import DocsByTree
from architecture.fragments import Fragment

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

class TestDocByTree(unittest.TestCase):

    def test_getSignature_shouldReturnCorrectSignature_whenSignatureInOneLine_withoutParameters(self):
        code_lines = ['class kek:']
        index = 0
        expected = "class kek"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), expected)

    def test_getSignature_shouldReturnCorrectSignature_whenSignatureInOneLine_withOneParameter(self):
        code_lines = ['class Kek(param):']
        index = 0
        expected = "class Kek(param)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), expected)

    def test_getSignature_shouldReturnCorrectSignature_whenSignatureInOneLine_withDefaultParameter(self):
        code_lines = ['def func(param=10):']
        index = 0
        expected = "def func(param=10)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), expected)

    def test_getSignature_shouldReturnCorrectSignature_whenSignatureInOneLine_withFewParameter(self):
        code_lines = ['class Kek(param1, param2, pararam100):']
        index = 0
        expected = "class Kek(param1, param2, pararam100)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), expected)

    def test_getSignature_shouldReturnCorrectSignature_whenSignatureInTwoLines(self):
        code_lines = ['class Kek(param1, ', 'param2, pararam100):']
        index = 0
        expected = "class Kek(param1, param2, pararam100)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), expected)

    def test_getSignature_shouldReturnCorrectSignature_whenSignatureInTwoLines_withNesting(self):
        code_lines = ['     class Kek(param1, ', '           param2, pararam100):']
        index = 0
        expected = "class Kek(param1, param2, pararam100)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), expected)

    def test_getSignature_shouldReturnCorrectSignature_whenSignatureInFewLines(self):
        code_lines = ['     class Kek(', 'param1,', '           param2,', 'pararam100):']
        index = 0
        expected = "class Kek(param1, param2, pararam100)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), expected)

    def test_getDocstring_shouldReturnCorrectDocstring_withDoubleQuotes(self):
        code_lines = ['" docstring "']
        index = 0
        expected = " docstring "
        self.assertEqual(DocsByTree.get_docstring(code_lines, index), expected)

    def test_getDocstring_shouldReturnCorrectDocstring_withSingleQuotes(self):
        code_lines = ["' docstring '"]
        index = 0
        expected = " docstring "
        self.assertEqual(DocsByTree.get_docstring(code_lines, index), expected)

    def test_getDocstring_shouldReturnCorrectDocstring_withTripleQuotes(self):
        code_lines = ['""" docstring """']
        index = 0
        expected = " docstring "
        self.assertEqual(DocsByTree.get_docstring(code_lines, index), expected)

    def test_getDocstring_shouldReturnCorrectDocstring_withFewLines(self):
        code_lines = ['"""docline1', 'docline2', 'docline3"""']
        index = 0
        expected = "docline1\ndocline2\ndocline3"
        self.assertEqual(DocsByTree.get_docstring(code_lines, index), expected)

    def test_getDocstring_shouldReturnCorrectDocstring_withFewLines(self):
        code_lines = ['"""docline1', 'docline2', 'docline3"""']
        index = 0
        expected = "docline1\ndocline2\ndocline3"
        self.assertEqual(DocsByTree.get_docstring(code_lines, index), expected)

    def test_getDocstring_shouldReturnCorrectDocstring_withRealCode(self):
        code_lines = ['    """docline1', '    docline2', '    docline3"""']
        index = 0
        expected = "docline1\ndocline2\ndocline3"
        self.assertEqual(DocsByTree.get_docstring(code_lines, index), expected)

    def test_getOnlyClassesNames_whenOnlyOneClass(self):
        code_lines = ['class Name:']
        expected = "Name"
        fragment = Fragment()
        self.assertEqual(DocsByTree.get_name())

if __name__ == "__main__":
    unittest.main()