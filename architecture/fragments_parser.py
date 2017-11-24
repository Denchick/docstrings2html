from . import code_fragment

class Parser:

    def __init__(self, codeLines):
        self.codeLines = codeLines
        self.keyWords = ['class', 'def']

    def parse_code_hierarchy(self, startLineIndex):
        nested_fragments = []
        parsed_code_fragments = []
        current_code_nesting = 0

        for line_index in range(len(self.codeLines)):
            line_nesting = self.get_nesting_of_line(self.codeLines[line_index])
            first_word_in_line = self.get_first_word_in_line(self.codeLines[line_index])

            if first_word_in_line == None:
                continue

            if current_code_nesting > line_nesting:
                fragment = nested_fragments.pop()
                fragment.lastCodeLine = line_index - 1
                parsed_code_fragments.append(fragment)
                current_code_nesting = line_nesting

            if first_word_in_line in self.keyWords:
                type = first_word_in_line
                fragment = code_fragment.CodeFragment(line_index, None, type, line_nesting)
                nested_fragments.append(fragment)
                current_code_nesting = line_nesting + 4

        while len(nested_fragments) > 0:
            fragment = nested_fragments.pop()
            fragment.lastCodeLine = len(self.codeLines) - 1
            parsed_code_fragments.append(fragment)

        return parsed_code_fragments

    def get_nesting_of_line(self, line):
        nesting = 0
        for char in line:
            if char == " ":
                nesting += 1
            else:
                break
        return nesting

    def line_starts_with_keyword(self, line):
        words_in_line = line.split()
        if len(words_in_line) == 0:
            return False
        return words_in_line[0] in self.keyWords

    def get_first_word_in_line(self, line):
        words = line.split()
        if len(words) == 0:
            return None
        return words[0]
