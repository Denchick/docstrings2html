""" Внутри построенного по коду дерева, этот модуль составляет
документацию для "компонента" кода. По сути - строит набор полей """

import re

from architecture import code_tree


class DocsByTree:
    def __init__(self, tree, code_lines, module_filename):
        if not isinstance(tree, code_tree.CodeTree):
            raise AttributeError
        self.tree = tree
        if not isinstance(code_lines, list):
            raise AttributeError

        self._documentation_nodes = []
        self.module_filename = module_filename
        self.code_lines = code_lines
        self._add_documentation(self.tree.get_root())

    def _add_documentation(self, tree_node):
        if not isinstance(tree_node, code_tree.TreeNode):
            raise AttributeError

        code_data = CodeData(tree_node.code_fragment,
                             self.module_filename,
                             self.get_signature(self.code_lines, tree_node.code_fragment.first_line),
                             self.get_docstring(self.code_lines, tree_node.code_fragment.first_line),
                             self.get_fragments_names_of_this_type(tree_node, 'class'),
                             self.get_fragments_names_of_this_type(tree_node, 'def'))

        self._documentation_nodes.append(code_data)
        for node in tree_node.nested_nodes:
            self._add_documentation(node)

    @staticmethod
    def get_signature(code_lines, signature_index):
        index = signature_index
        result = ''
        while True:
            current_line = code_lines[index].strip()
            result += current_line
            if current_line.endswith(':'):
                break
            if result.endswith(','):
                result += ' '
            index += 1
        return result[:-1]

    @staticmethod
    def get_docstring(code_lines, signature_index):
        code = '\n'.join(code_lines[signature_index:])

        pattern1 = r'^\s*"""([\w\s.,\/#!$%\^&\*;:{}=\-_`~()]*)"""'
        pattern2 = r'^\s*"([\w\s.,\/#!$%\^&\*;:{}=\-_`~()]*)"'
        pattern3 = r"^\s*'([\w\s.,\/#!$%\^&\*;:{}=\-_`~()]*)'"
        result = re.search(pattern1, code)
        if result:
            return result.group(1)
        result = re.search(pattern2, code)
        if result:
            return result.group(1)
        result = re.search(pattern3, code)
        if result:
            return result.group(1)
        return result



    def get_documentation_nodes(self):
        return self._documentation_nodes

    def get_fragments_names_of_this_type(self, tree_node, type):
        if not isinstance(type, str):
            raise AttributeError
        return [ self.get_name(f.code_fragment, 'kek') for f in tree_node.nested_nodes if f.code_fragment.type == type]

    @staticmethod
    def get_name(self, signature):
        # переделать!
        return 'signature'
        pattern = "def ([\s\w]*)\(([\s\w!\"#$%&\'()*+,\-\./:;<=>?@[\\\]^_`{|}~]*)\):"
        result = re.search(pattern, signature)
        return result.group(0)
        #return self.code_lines[fragment.first_line].strip().replace(':', ' ').replace('(', ' ').split()[1]


class CodeData:
    def __init__(self, fragment, filename, signature, docstring, classes, functions):
        self.fragment = fragment
        self.filename = filename
        self.signature = signature
        self.docstring = docstring
        self.classes = classes
        self.functions = functions