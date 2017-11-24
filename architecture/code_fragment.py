class CodeFragment:
    def __init__(self, firstCodeLine, lastCodeLine, typeFragment, nesting):
        self.firstCodeLine = firstCodeLine
        self.lastCodeLine = lastCodeLine
        self.typeFragment = typeFragment
        self.nesting = nesting

    def define_type_fragment(self, firstLine):
        for keyWord in self.keyWords:
            if self.codeLines[firstLine].startswith(keyWord):
                return keyWord
        raise RuntimeError("Unknown type fragment: {0} {1}")

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__