import unittest
import os
import sys

from architecture.fragments import Fragment

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from architecture.docs_by_tree import DocsByTree, CodeData


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
        self.assertEqual(DocsByTree._get_docstring(code_lines, index), expected)

    def test_getDocstring_shouldReturnCorrectDocstring_withSingleQuotes(self):
        code_lines = ["'docstring'"]
        index = 0
        expected = "docstring"
        self.assertEqual(DocsByTree._get_docstring(code_lines, index), expected)

    def test_getDocstring_shouldReturnCorrectDocstring_withTripleQuotes(self):
        code_lines = ['""" docstring """']
        index = 0
        expected = " docstring "
        self.assertEqual(DocsByTree._get_docstring(code_lines, index), expected)

    def test_getDocstring_shouldReturnCorrectDocstring_withFewLines(self):
        code_lines = ['"""docline1', 'docline2', 'docline3"""']
        index = 0
        expected = "docline1\ndocline2\ndocline3"
        self.assertEqual(DocsByTree._get_docstring(code_lines, index), expected)

    def test_getDocstring_shouldReturnCorrectDocstring_withRealCode(self):
        code_lines = ['    """docline1', '    docline2', '    docline3"""']
        index = 0
        expected = "docline1\ndocline2\ndocline3"
        self.assertEqual(DocsByTree._get_docstring(code_lines, index), expected)

    def test_module_description_when_no_description(self):
        source_code = "#!/usr/bin/env python3"
        expected = ''
        self.assertEqual(DocsByTree.get_module_description(source_code), expected)

    def test_module_description_when_no_description2(self):
        source_code = ''
        expected = ''
        self.assertEqual(DocsByTree.get_module_description(source_code), expected)

    def test_module_description_when_no_description3(self):
        source_code = 'sm text'
        expected = ''
        self.assertEqual(DocsByTree.get_module_description(source_code), expected)

    def test_module_description_when_there_is_description_in_the_top(self):
        source_code = """\"\"\"Description\"\"\"
        some code"""
        expected = 'Description'
        self.assertEqual(DocsByTree.get_module_description(source_code), expected)

    def test_module_description_when_there_is_description_not_in_the_top_but_first(self):
        source_code = """
        
        \"\"\"Description\"\"\"
        some code"""
        expected = 'Description'
        self.assertEqual(DocsByTree.get_module_description(source_code), expected)

    def test_module_description_when_there_is_description_not_in_the_top_but_not_first(self):
        source_code = """#!/usr/bin/env python3

        \"\"\"Description\"\"\"
        some code"""
        expected = 'Description'
        self.assertEqual(DocsByTree.get_module_description(source_code), expected)

    def test_CodeDataConstructor_shouldRaiseError_whenFragmentIsNotFragment(self):
        with self.assertRaises(AttributeError):
            CodeData('kek', 'kek', 'kek', 'kek', 'kek')

    def test_CodeDataConstructor_shouldRaiseError_whenModuleNameIsNotStr(self):
        with self.assertRaises(AttributeError):
            CodeData(Fragment(0, 0, '', 0), 0, 0, 0, 0)

    def test_CodeDataConstructor_shouldRaiseError_whenSignatureIsNotStr(self):
        with self.assertRaises(AttributeError):
            CodeData(Fragment(0, 0, '', 0), 'module_name', 0, 0, 0)

    def test_CodeDataConstructor_shouldRaiseError_whenDocstringIsNotStr(self):
        with self.assertRaises(AttributeError):
            CodeData(Fragment(0, 0, '', 0), 'module_name', 'signature', 0, 0)

    def test_CodeDataConstructor_shouldRaiseError_whenParentSignatureIsNotStr(self):
        with self.assertRaises(AttributeError):
            CodeData(Fragment(0, 0, '', 0), 'module_name', 'signature', 'doc', 0)

    def test_CodeData_getName_ShouldReturnCorrectName(self):
        self.assertEqual(CodeData._get_name('class signature:'), 'signature')

    def test_CodeData_getName_ShouldReturnNone_whenNotClassOrDef(self):
        self.assertEqual(CodeData._get_name('kek signature:'), None)

    def test_CodeDataProperties(self):
        cd = CodeData(Fragment(0, 0, '', 0), 'module_name', 'class signature', 'docstring', 'class parent_name:')
        self.assertEqual(cd.parent_name, 'parent_name')
        self.assertEqual(cd.docstring, 'docstring')
        self.assertEqual(cd.signature, 'class signature')
        self.assertEqual(cd.module_name, 'module_name')
        self.assertEqual(cd.name, 'parent_name.signature')
        self.assertEqual(cd.docstring, 'docstring')

if __name__ == "__main__":
    unittest.main()