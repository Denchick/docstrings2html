from architecture import code_tree


class Documentation4Fragmnets:
    def __init__(self, tree, code_lines, filename):
        if not isinstance(tree, code_tree.CodeTree):
            raise AttributeError
        self.tree = tree
        if not isinstance(code_lines, list):
            raise AttributeError

        self._documentation_nodes = []
        self.add_documentation(self.tree.get_root())
        self.filename = filename

    def add_documentation(self, tree_node):
        if not isinstance(tree_node, code_tree.TreeNode):
            raise AttributeError

        code_data = CodeData(self.filename,
                             self.get_signature(tree_node),
                             self.get_docstring(tree_node),
                             self.get_only_classes(tree_node),
                             self.get_only_classes(tree_node))

        for node in tree_node.nested_nodes:
            self.add_documentation(node)

    def get_signature(self, tree_node):
        if not isinstance(tree_node, code_tree.TreeNode):
            raise AttributeError


    def get_documentation_nodes(self):
        return self._documentation_nodes

    def get_docstring(self, tree_node):
        pass


class CodeData:
    def __init__(self, filename, signature, docstring, classes, functions):
        self.filename = filename
        self.signature = signature
        self.docstring = docstring
        self.classes = classes
        self.functions = functions