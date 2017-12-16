from architecture import code_tree


class Documentation4Fragmnets:
    def __init__(self, tree, code_lines, filename):
        if not isinstance(tree, code_tree.CodeTree):
            raise AttributeError
        self.tree = tree
        if not isinstance(code_lines, list):
            raise AttributeError

        self._documentation_nodes = []
        self.filename = filename
        self.code_lines = code_lines
        self.add_documentation(self.tree.get_root())

    def add_documentation(self, tree_node):
        if not isinstance(tree_node, code_tree.TreeNode):
            raise AttributeError

        code_data = CodeData(tree_node.code_fragment,
                             self.filename,
                             self.get_signature(tree_node),
                             self.get_docstring(tree_node),
                             self.get_only_classes_names(tree_node),
                             self.get_only_functions_names(tree_node))

        self._documentation_nodes.append(code_data)
        for node in tree_node.nested_nodes:
            self.add_documentation(node)

    def get_signature(self, tree_node):
        if not isinstance(tree_node, code_tree.TreeNode):
            raise AttributeError
        signature_index = tree_node.code_fragment.first_line
        return self.code_lines[signature_index].strip()

    def get_docstring(self, tree_node):
        index = tree_node.code_fragment.first_line + 1
        result = []
        while True:
            current_line = self.code_lines[index]
            result.append(current_line)
            if current_line.endswith('"""'):
                break
            index += 1
        return '\n'.join(result)

    def get_documentation_nodes(self):
        return self._documentation_nodes

    def get_only_classes_names(self, tree_node):
        return [ self.get_name(fragment) for fragment in tree_node.code_fragment if fragment.type == 'class']

    def get_only_functions_names(self, tree_node):
        return [ self.get_name(fragment) for fragment in tree_node.code_fragment if fragment.type == 'def']

    def get_name(self, fragment):
        return self.code_lines[fragment.first_line].strip().replace(':', ' ').replace('(', ' ').split()[1]


class CodeData:
    def __init__(self, fragment, filename, signature, docstring, classes, functions):
        self.fragment = fragment
        self.filename = filename
        self.signature = signature
        self.docstring = docstring
        self.classes = classes
        self.functions = functions