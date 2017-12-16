from architecture import code_tree


class ToHtml:
    def __init__(self, code_lines, tree):
        """
        Формирует HTML-страничку по parsed_code_fragments
        :param code_lines: список строк кода
        :param parsed_code_fragments: список CodeFragments - фрагментов кода
        """

        if not isinstance(tree, code_tree.CodeTree):
            raise AttributeError

        self.tree = tree


    def get_classes_fragments
