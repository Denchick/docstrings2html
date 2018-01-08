import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from architecture.code_tree import CodeTree
from architecture.docs_by_tree import DocsByTree
from architecture.html_builder import HtmlBuilder


class TestHtmlBuilder(unittest.TestCase):
    def test_htmlCode_containsDocstring_afterFunctionDefinition(self):
        code_lines = ['def func(f1, f2):', '    """THIS IS DOCSTRING"""']
        source_code = '\n'.join(code_lines)

        tree = CodeTree(code_lines)
        docs = DocsByTree(tree, code_lines, source_code, '')
        self.html_builder = HtmlBuilder(docs, '', '')
        html_code = self.html_builder.get_html()

        self.assertTrue(html_code.count('THIS IS DOCSTRING') > 1)

    def test_htmlCode_containsDocstring_afterClassDefinition(self):
        code_lines = ['class MyClass:', '    """THIS IS DOCSTRING"""']
        source_code = '\n'.join(code_lines)

        tree = CodeTree(code_lines)
        docs = DocsByTree(tree, code_lines, source_code, '')
        self.html_builder = HtmlBuilder(docs, '', '')
        html_code = self.html_builder.get_html()

        self.assertTrue(html_code.count('THIS IS DOCSTRING') > 1)

    def test_htmlCode_doesNotContainExtraDocstring(self):
        code_lines = ['p = 13', '"""THIS IS NOT DOCSTRING"""',
                      'class MyClass:', '    pass', '']
        source_code = '\n'.join(code_lines)

        tree = CodeTree(code_lines)
        docs = DocsByTree(tree, code_lines, source_code, '')
        self.html_builder = HtmlBuilder(docs, '', '')
        html_code = self.html_builder.get_html()

        self.assertTrue(html_code.count('THIS IS NOT DOCSTRING') == 1)


if __name__ == '__main__':
    unittest.main()
