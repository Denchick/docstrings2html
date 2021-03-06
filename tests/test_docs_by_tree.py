import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from architecture.docs_by_tree import DocsByTree
from architecture.docs_by_tree import CodeData
from architecture.fragments import Fragment


class TestDocByTree(unittest.TestCase):

    def test_getSignature_whenSignatureInOneLine_withoutParameters(self):
        code_lines = ['class kek:']
        index = 0
        exp = "class kek"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), exp)

    def test_getSignature_whenSignatureInOneLine_withOneParameter(self):
        code_lines = ['class Kek(param):']
        index = 0
        exp = "class Kek(param)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), exp)

    def test_getSignature_whenSignatureInOneLine_withDefaultParameter(self):
        code_lines = ['def func(param=10):']
        index = 0
        exp = "def func(param=10)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), exp)

    def test_getSignature_whenSignatureInOneLine_withFewParameter(self):
        code_lines = ['class Kek(param1, param2, pararam100):']
        index = 0
        exp = "class Kek(param1, param2, pararam100)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), exp)

    def test_getSignature_whenSignatureInTwoLines(self):
        code_lines = ['class Kek(param1, ', 'param2, pararam100):']
        index = 0
        exp = "class Kek(param1, param2, pararam100)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), exp)

    def test_getSignature_whenSignatureInTwoLines_withNesting(self):
        code_lines = ['     class Kek(param1, ',
                      '           param2, pararam100):']
        index = 0
        exp = "class Kek(param1, param2, pararam100)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), exp)

    def test_getSignature_whenSignatureInFewLines(self):
        code_lines = ['     class Kek(', 'param1,',
                      '           param2,', 'pararam100):']
        index = 0
        exp = "class Kek(param1, param2, pararam100)"
        self.assertEqual(DocsByTree.get_signature(code_lines, index), exp)

    def test_getDocstring_shouldReturnCorrectDocstring_withDoubleQuotes(self):
        code_lines = ['" docstring "']
        index = 0
        exp = " docstring "
        self.assertEqual(DocsByTree._get_docstring(code_lines, index), exp)

    def test_getDocstring_shouldReturnCorrectDocstring_withSingleQuotes(self):
        code_lines = ["'docstring'"]
        index = 0
        exp = "docstring"
        self.assertEqual(DocsByTree._get_docstring(code_lines, index), exp)

    def test_getDocstring_shouldReturnCorrectDocstring_withTripleQuotes(self):
        code_lines = ['""" docstring """']
        index = 0
        exp = " docstring "
        self.assertEqual(DocsByTree._get_docstring(code_lines, index), exp)

    def test_getDocstring_shouldReturnCorrectDocstring_withFewLines(self):
        code_lines = ['"""docline1', 'docline2', 'docline3"""']
        index = 0
        exp = "docline1\ndocline2\ndocline3"
        self.assertEqual(DocsByTree._get_docstring(code_lines, index), exp)

    def test_getDocstring_shouldReturnCorrectDocstring_withRealCode(self):
        code_lines = ['    """docline1', '    docline2', '    docline3"""']
        index = 0
        exp = "docline1\ndocline2\ndocline3"
        self.assertEqual(DocsByTree._get_docstring(code_lines, index), exp)

    def test_moduleDescription_whenNoDescription(self):
        source_code = "#!/usr/bin/env python3"
        exp = ''
        self.assertEqual(DocsByTree.get_module_description(source_code), exp)

    def test_moduleDescription_whenNoDescription2(self):
        source_code = ''
        exp = ''
        self.assertEqual(DocsByTree.get_module_description(source_code), exp)

    def test_moduleDescription_whenNoDescription3(self):
        source_code = 'sm text'
        exp = ''
        self.assertEqual(DocsByTree.get_module_description(source_code), exp)

    def test_moduleDescription_whenThereIsDescriptionInTheTop(self):
        source_code = """'Description'
        some code"""
        exp = 'Description'
        self.assertEqual(DocsByTree.get_module_description(source_code), exp)

    def test_moduleDescription_whenThereIsDescriptionNotInTopButFirst(self):
        source_code = """

        \"\"\"Description\"\"\"
        some code"""
        exp = ''
        self.assertEqual(DocsByTree.get_module_description(source_code), exp)

    def test_moduleDescription_whenThereIsDescrptionNotInTopAndNotFirst(self):
        source_code = """#!/usr/bin/env python3

        \"\"\"Description\"\"\"
        some code"""
        exp = ''
        self.assertEqual(DocsByTree.get_module_description(source_code), exp)

    def test_moduleDescription_whenThereIsDescriptionButNotFirst(self):
        source_code = """#!/usr/bin/env python3
        class kek:
            \"\"\"Description\"\"\"
            some code"""
        exp = ''
        self.assertEqual(DocsByTree.get_module_description(source_code), exp)

    def test_CodeDataConstructor_shouldRaiseError_whenNotFragment(self):
        with self.assertRaises(AttributeError):
            CodeData('kek', 'kek', 'kek', 'kek', 'kek')

    def test_CodeDataConstructor_shouldRaiseError_whenModleNameIsNotStr(self):
        with self.assertRaises(AttributeError):
            CodeData(Fragment(0, 0, '', 0), 0, 0, 0, 0)

    def test_CodeDataConstructor_shouldRaiseError_whenSignatureIsNotStr(self):
        with self.assertRaises(AttributeError):
            CodeData(Fragment(0, 0, '', 0), 'module_name', 0, 0, 0)

    def test_CodeDataConstructor_shouldRaiseError_whenDocstringIsNotStr(self):
        with self.assertRaises(AttributeError):
            CodeData(Fragment(0, 0, '', 0), 'module_name', 'signature', 0, 0)

    def test_constructor_shouldRaiseError_whenParentSignatureIsNotStr(self):
        with self.assertRaises(AttributeError):
            CodeData(Fragment(0, 0, '', 0), 'module_name',
                     'signature', 'doc', 0)

    def test_CodeData_getName_ShouldReturnCorrectName(self):
        self.assertEqual(CodeData._get_name('class signature:'), 'signature')

    def test_CodeData_getName_ShouldReturnNone_whenNotClassOrDef(self):
        self.assertEqual(CodeData._get_name('kek signature:'), '')

    def test_CodeDataProperties(self):
        cd = CodeData(Fragment(0, 0, '', 0), 'module_name', 'class signature',
                      'docstring', 'class parent_name:')
        self.assertEqual(cd.parent_name, 'parent_name')
        self.assertEqual(cd.docstring, 'docstring')
        self.assertEqual(cd.signature, 'class signature')
        self.assertEqual(cd.module_name, 'module_name')
        self.assertEqual(cd.name, 'parent_name.signature')
        self.assertEqual(cd.docstring, 'docstring')


if __name__ == "__main__":
    unittest.main()
