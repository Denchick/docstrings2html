""" По разбитым фрагментам кода строится дерево его "компонентов"
 по вложенности друг в друга"""

from architecture.fragments import Fragment, FragmentsParser


class TreeNode:
    def __init__(self, code_fragment, nested_nodes=None):
        self.code_fragment = code_fragment
        self.nested_nodes = [] if nested_nodes is None else nested_nodes

    def add_fragment(self, code_fragment):
        if not isinstance(code_fragment, Fragment):
            message = "code_fragments expected Fragment but got {0}".format(
                type(code_fragment))
            raise AttributeError(message)

        if not self.nested_nodes:
            self.nested_nodes.append(TreeNode(code_fragment))
            return

        index = self._find_where_to_insert_node(code_fragment)
        if (index == len(self.nested_nodes)):
            self.nested_nodes.append(TreeNode(code_fragment))
            return
        current_fragment = self.nested_nodes[index].code_fragment
        if current_fragment.first_line <= code_fragment.first_line and \
                        code_fragment.last_line <= current_fragment.last_line:
            self.nested_nodes[index].add_fragment(code_fragment)
            return
        self.nested_nodes.insert(index, TreeNode(code_fragment))

    def _find_where_to_insert_node(self, fragment):
        if not isinstance(fragment, Fragment):
            message = "Expected get Fragment type, but {0}".format(
                type(fragment))
            AttributeError(message)

        if not self.nested_nodes or \
                        fragment.last_line <= \
                        self.nested_nodes[0].code_fragment.first_line:
            return 0
        if self.nested_nodes[-1].code_fragment.last_line <= \
                fragment.first_line:
            return len(self.nested_nodes)

        for i in range(len(self.nested_nodes)):
            current_node = self.nested_nodes[i]
            current_fragment = current_node.code_fragment

            # засунуть вовнутрь
            if current_fragment.first_line <= fragment.first_line and \
                            fragment.last_line <= current_fragment.last_line:
                return i

            next_fragment = self.nested_nodes[i + 1].code_fragment
            #засунуть сразу после
            if current_fragment.last_line <= fragment.first_line and \
                fragment.last_line <= next_fragment.first_line:
                return i + 1

        raise RuntimeError("Didnt find where to insert")

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__



class CodeTree:

    def __init__(self, code_lines):
        """
        Иерархическое дерево кода

        :param code_lines_count: количество строк в тектовом файле
        """
        fragment = Fragment(0, len(code_lines), 'file', 0)
        self._root = TreeNode(fragment)
        self.code_lines = code_lines
        parser = FragmentsParser(code_lines)
        fragments_list = parser.parse_code_lines()
        fragments_list.sort(key=lambda f: (f.first_line, -f.last_line))
        for fragment in fragments_list:
            self._root.add_fragment(fragment)

    def get_root(self):
        return self._root