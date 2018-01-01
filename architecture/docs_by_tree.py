""" Внутри построенного по коду дерева, этот модуль составляет
документацию code fragments. По сути - строит набор полей """

import re
from architecture import code_tree
from architecture.fragments import Fragment


class DocsByTree:
    """ Формирует список CodeData по построенному дереву кода """
    def __init__(self, tree, code_lines, code, module_name):
        error_message = '{0} must be a {1} type, but got type {2}'
        if not isinstance(tree, code_tree.CodeTree):
            raise AttributeError(error_message.format('tree',
                                                      'CodeTree',
                                                      type(tree)))
        if not isinstance(code_lines, list):
            raise AttributeError(error_message.format('code_lines',
                                                      'list',
                                                      type(code_lines)))
        self.tree = tree
        self._documentation_nodes = []
        self.code = code
        self.module_description = self.get_module_description(self.code)
        self.module_name = ''
        if module_name:
            self.module_name = \
                module_name.replace('\\', ' ').replace('/', ' ').split()[-1]

        self.code_lines = code_lines
        self._add_documentation(self.tree.get_root(), None)

    def _add_documentation(self, node, parent_node):
        """ Добавляет документацию по node(TreeNode) в список self._documentation_nodes
        Для каждого ребенка текущего node вызывается метод self._add_documentation
        с соответствующими параметрами """

        error_message = '{0} must be a TreeNode type, but got type {1}'
        if not isinstance(node, code_tree.TreeNode):
            raise AttributeError(error_message.format('node', type(node)))
        if parent_node and not isinstance(parent_node, code_tree.TreeNode):
            raise AttributeError(error_message.format('parent_node',
                                                      type(parent_node)))
        if parent_node:
            parent = self.get_signature(self.code_lines,
                                        parent_node.code_fragment.first_line)
        else:
            parent = ''
        code_data = CodeData(node.code_fragment,
                             self.module_name,
                             self.get_signature(
                                 self.code_lines,
                                 node.code_fragment.first_line),
                             self._get_docstring(
                                 self.code_lines,
                                 node.code_fragment.first_line),
                             parent)

        if code_data.name.startswith('__') and code_data.name != '__init__':
            return

        self._documentation_nodes.append(code_data)
        for current_node in node.nested_nodes:
            self._add_documentation(current_node, node)

    @staticmethod
    def get_signature(code_lines, signature_index):
        """ Достает сигнатуру метода. Для деталей работы смотри тесты
        из test_docs_by_tree.py.

        Args:
            code_lines (list<str>): исходный код модуля
                в виде списка строк
            signature_index (int): индекс строки, в которой
                начинается сигнатура метода

        Returns:
            Корректную сигнатуру метода в виде одной строки
            без отступов, множественных пробелов и переносов строк
        """
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

    def get_all_methods_from_nodes(self):
        return [doc_node
                for doc_node in self.documentation_nodes
                if doc_node.type == 'def']

    def get_all_classes_from_nodes(self):
        return [doc_node
                for doc_node in self.documentation_nodes
                if doc_node.type == 'class']

    @staticmethod
    def _get_docstring(code_lines, signature_index):
        """ Достает docstrings сразу после сигнатуры метода.
        Для деталей работы смотри тесты из test_docs_by_tree.

        Args:
            code_lines (list<str>): исходный код модуля
                в виде списка строк
            signature_index (int): индекс строки, в которой
                начинается сигнатура метода

        Returns:
            Коректный docstring в виде одной строки, без ковычек
            и отступа перед docstring. Для деталей смотри
            test_docs_by_tree.py
        """
        docstring = DocsByTree._get_raw_docstring(code_lines, signature_index)
        nesting = len(docstring) - len(docstring.lstrip())
        lines = [line[nesting:].strip('"\'') for line in docstring.split('\n')]
        return '\n'.join(lines)

    @staticmethod
    def _get_raw_docstring(code_lines, signature_index):
        """ Просто получает первую строку внутри двойных, тройных или
        одинарных ковычек - что попадется раньше. Никак не
        обрабатывает получученный текст, просто его возвращает.

        Args:
            code_lines (list<str>): исходный код модуля
                в виде списка строк
            signature_index (int): индекс строки, в которой
                начинается сигнатура метода

        Returns:
            Первое совпадение с шаблоном docstring - первый
            текст внутри кавычек. Если ничего нет, возвращается
            пустая строка.
        """
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
        return ''

    @property
    def documentation_nodes(self):
        return self._documentation_nodes

    @staticmethod
    def get_module_description(module_source_code):
        pattern1 = r'[\ ]*"""([\S\s]*?)"""'
        pattern2 = r'[\ ]*"([\S\s]*?)"'
        pattern3 = r"[\ ]*'([\S\s]*?)'"

        result = re.match(pattern1, module_source_code)
        if result:
            return result.group(1)
        result = re.match(pattern2, module_source_code)
        if result:
            return result.group(1)
        result = re.match(pattern3, module_source_code)
        if result:
            return result.group(1)
        return ''

class CodeData:
    def __init__(self,
                 fragment,
                 module_name,
                 signature,
                 docstring,
                 parent_signature):
        """ Единица сформированный документации. По сути -
        просто объект с набором полей для хранения. """
        error_msg = '{0} must be a {1} type, but got type {2}'
        if not isinstance(fragment, Fragment):
            raise AttributeError(error_msg.format('"fragment"',
                                                  'Fragment',
                                                  type(fragment)))
        self._fragment = fragment
        if not isinstance(module_name, str):
            raise AttributeError(error_msg.format('"module_name"',
                                                  'str',
                                                  type(module_name)))
        self._module_name = module_name
        if not isinstance(signature, str):
            raise AttributeError(error_msg.format('"signature"',
                                                  'str',
                                                  type(signature)))
        self._signature = signature
        if not isinstance(docstring, str):
            raise AttributeError(error_msg.format('"docstring"',
                                                  'str',
                                                  type(docstring)))
        self._docstring = docstring
        if not isinstance(parent_signature, str):
            raise AttributeError(error_msg.format('"parent_signature"',
                                                  'str',
                                                  type(parent_signature)))
        self._parent_name = self._get_name(parent_signature) if fragment.type != 'file' else ''

    @staticmethod
    def _get_name(signature):
        """ Название фрагмента CodeData.
        Если функция или класс, то соответсвенно его название.
        Если целый файл, то его название. """
        if signature.startswith('def') or signature.startswith('class'):
            new_sign = signature.replace('(', ' ').replace(':', ' ')
            return new_sign.split()[1]
        return ''

    @property
    def module_name(self):
        return self._module_name

    @property
    def signature(self):
        return self._signature

    @property
    def docstring(self):
        return self._docstring

    @property
    def parent_name(self):
        return self._parent_name

    @property
    def type(self):
        return self._fragment.type

    @property
    def name(self):
        if self.parent_name:
            return '{0}.{1}'.format(self.parent_name,
                                    self._get_name(self.signature))
        return self._get_name(self.signature)

    def get_annotation(self):
        """ Короткое описание CodeData """
        annotation = self._docstring.split('.')
        if len(annotation) > 0:
            return annotation[0]
        return ''