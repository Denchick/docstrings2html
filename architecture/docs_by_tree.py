""" Внутри построенного по коду дерева, этот модуль составляет
документацию для "компонента" кода. По сути - строит набор полей """

import re

from architecture import code_tree


class DocsByTree:
    def __init__(self, tree, code_lines, code, module_name):
        if not isinstance(tree, code_tree.CodeTree):
            raise AttributeError
        self.tree = tree
        if not isinstance(code_lines, list):
            raise AttributeError

        self._documentation_nodes = []
        self.code = code
        self.module_description = self.get_module_description()
        self.module_filename = ''
        if module_name:
            self.module_filename = module_name.replace('\\', ' ').replace('/', ' ').split()[-1]
        self.code_lines = code_lines
        self._add_documentation(self.tree.get_root(), None)

    def _add_documentation(self, node, parent_node):
        if not isinstance(node, code_tree.TreeNode):
            raise AttributeError
        if parent_node is not None and not isinstance(parent_node, code_tree.TreeNode):
            raise AttributeError

        code_data = CodeData(node.code_fragment,
                             self.module_filename,
                             self._get_signature(self.code_lines, node.code_fragment.first_line),
                             self._get_docstring(self.code_lines, node.code_fragment.first_line),
                             self.get_fragments_names_of_this_type(node, 'class'),
                             self.get_fragments_names_of_this_type(node, 'def'),
                             self.get_tree_node_name(parent_node))

        self._documentation_nodes.append(code_data)
        for current_node in node.nested_nodes:
            self._add_documentation(current_node, node)

    @staticmethod
    def _get_signature(code_lines, signature_index):
        index = signature_index
        result = ''
        while index < len(code_lines):
            current_line = code_lines[index].strip()
            result += current_line
            if current_line.endswith(':'):
                break
            if result.endswith(','):
                result += ' '
            index += 1
        return result[:-1]

    def get_methods(self):
        return [doc_node for doc_node in self.get_documentation_nodes() if doc_node.fragment.type == 'def']

    def get_classes(self):
        return [doc_node for doc_node in self.get_documentation_nodes() if doc_node.fragment.type == 'class']

    @staticmethod
    def _get_docstring(code_lines, signature_index):
        docstring = DocsByTree._get_raw_docstring(code_lines, signature_index)
        nesting = len(docstring) -len(docstring.lstrip())
        lines = [DocsByTree._get_docstring_without_quotes(line[nesting:])  for line in docstring.split('\n')]
        return '\n'.join(lines)

    @staticmethod
    def _get_raw_docstring(code_lines, signature_index):
        code = '\n'.join(code_lines[signature_index:])

        pattern1 = r'([\ ]*"""[\S\s]*?""")'
        pattern2 = r'([\ ]*"[\S\s]*?")'
        pattern3 = r"([\ ]*'[\S\s]*?')"
        re_result = re.search(pattern1, code)
        if re_result:
            return re_result.group(1)
        re_result = re.search(pattern2, code)
        if re_result:
            return re_result.group(1)
        re_result = re.search(pattern3, code)
        if re_result:
            return re_result.group(1)
        return "empty"

    @staticmethod
    def _get_docstring_without_quotes(docstring):
        return docstring.strip('"\'')

    def get_documentation_nodes(self):
        return self._documentation_nodes

    def get_fragments_names_of_this_type(self, tree_node, type):
        if not isinstance(type, str):
            raise AttributeError
        return [self._get_name(f.code_fragment, 'kek') for f in tree_node.nested_nodes if f.code_fragment.type == type]

    @staticmethod
    def _get_name(self, signature):
        # переделать!
        return 'signature'
        pattern1 = "def ([\s\w]*)\(([\s\w!\"#$%&\'()*+,\-\./:;<=>?@[\\\]^_`{|}~]*)\):"
        result = re.search(pattern, signature).group(0)
        if result:
            return result
        pattern2 = "class ([\s\w]*)\(([\s\w!\"#$%&\'()*+,\-\./:;<=>?@[\\\]^_`{|}~]*)\):"
        result = re.search(pattern, signature).group(0)
        if result:
            return result
        return 'елки-палки, дичь какая-то! ' + signature
        #return self.code_lines[fragment.first_line].strip().replace(':', ' ').replace('(', ' ').split()[1]

    def get_module_description(self):
        pattern1 = r'^\s*"""([\w\s.,\/#!$%\^&\*;:{}=\-_`~()]*)"""'
        pattern2 = r'^\s*"([\w\s.,\/#!$%\^&\*;:{}=\-_`~()]*)"'
        pattern3 = r"^\s*'([\w\s.,\/#!$%\^&\*;:{}=\-_`~()]*)'"
        result = re.search(pattern1, self.code)
        if result:
            return result.group(1)
        result = re.search(pattern2, self.code)
        if result:
            return result.group(1)
        result = re.search(pattern3, self.code)
        if result:
            return result.group(1)
        return result

    def get_tree_node_name(self, tree_node):
        if tree_node is None:
            return ''
        first_line = self.code_lines[tree_node.code_fragment.first_line]
        first_line = first_line.replace(':', ' ').replace('(', ' ')
        if 'def' in first_line or 'class' in first_line:
            return first_line.split()[1]

class CodeData:
    def __init__(self, fragment, filename, signature, docstring, classes, functions, parent_name):
        self.fragment = fragment
        self.filename = filename
        self.signature = signature
        self.docstring = docstring
        self.classes = classes
        self.functions = functions
        self.parent_name = parent_name

    def get_annotation(self):
        """ короткое описание фрагмента """
        annotation = self.docstring.split('.')
        if len(annotation) > 0:
            return annotation[0]
        return ''

    def get_docstring(self):
        return self.docstring

    def get_name(self):
        if self.signature.startswith('def') or self.signature.starts_with('class'):
            signature = self.signature.replace('(', ' ').replace(':', ' ').split()[1]
            if self.parent_name:
                return "{0}.{1}".format(self.parent_name, signature)
            return  signature
