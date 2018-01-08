import unittest

from architecture.code_tree import CodeTree
from architecture.docs_by_tree import DocsByTree
from architecture.html_builder import HtmlBuilder


class TestHtmlBuilder(unittest.TestCase):
    def test_html_code_contains_docstring_after_function_definition(self):
        code_lines = ['def func(f1, f2):', '    """THIS IS DOCSTRING"""']
        source_code = '\n'.join(code_lines)

        tree = CodeTree(code_lines)
        docs = DocsByTree(tree, code_lines, source_code, '')
        self.html_builder = HtmlBuilder(docs, '', '')
        html_code = self.html_builder.get_html()

        self.assertTrue(html_code.count('THIS IS DOCSTRING') > 1)

    def test_html_code_contains_docstring_under_class_definition(self):
        code_lines = ['class MyClass:', '    """THIS IS DOCSTRING"""']
        source_code = '\n'.join(code_lines)

        tree = CodeTree(code_lines)
        docs = DocsByTree(tree, code_lines, source_code, '')
        self.html_builder = HtmlBuilder(docs, '', '')
        html_code = self.html_builder.get_html()

        self.assertTrue(html_code.count('THIS IS DOCSTRING') > 1)

    def test_html_code_does_not_contain_docstring_that_does_not_belong_this_fragment(self):
        code_lines = ['p = 13', '"""THIS IS NOT DOCSTRING"""', 'class MyClass:', '    pass', '']
        source_code = '\n'.join(code_lines)

        tree = CodeTree(code_lines)
        docs = DocsByTree(tree, code_lines, source_code, '')
        self.html_builder = HtmlBuilder(docs, '', '')
        html_code = self.html_builder.get_html()
        c = html_code.count('THIS IS NOT DOCSTRING')

        self.assertTrue(c == 1)

if __name__ == '__main__':
    unittest.main()
