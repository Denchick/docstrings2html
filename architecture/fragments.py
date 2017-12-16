
class Fragment:

    def __init__(self, first_line: int, last_line: int, type_fragment: str, nesting: int):
        """
        Один логический кусок кода - функция, класс или весь файл

        :param first_line: номер строчки кода, с которой начинается фрагмент
        :param last_line: номер строчки кода, на которой заканчивается фрагмент
        :param type_fragment: тип этого фрагмента - класс, функция, etc
        :param nesting: вложенность фрагмента - количество "пробелов" перед сигнатурой фрагмента
        """
        self.first_line = first_line
        self.last_line = last_line
        self.type = type_fragment
        self.nesting = nesting

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__




class FragmentsParser:

    def __init__(self, code_lines):
        """
        Парсер кода на фрагменты
        :param code_lines: список строк кода
        """
        self.code_lines = code_lines
        self.key_words = ['class', 'def']

    def parse_code_lines(self):
        nested_fragments = []
        parsed_fragments = []
        current_code_nesting = 0

        for line_index in range(len(self.code_lines)):
            line_nesting = self.get_nesting_of_line(self.code_lines[line_index])
            first_word_in_line = self.get_first_word_in_line(self.code_lines[line_index])

            if first_word_in_line == None:
                continue

            if current_code_nesting > line_nesting:
                fragment = nested_fragments.pop()
                fragment.last_line = line_index - 1
                parsed_fragments.append(fragment)
                current_code_nesting = line_nesting

            if first_word_in_line in self.key_words:
                type = first_word_in_line
                fragment = Fragment(line_index, None, type, line_nesting)
                nested_fragments.append(fragment)
                current_code_nesting = line_nesting + 4

        while len(nested_fragments) > 0:
            fragment = nested_fragments.pop()
            fragment.last_line = len(self.code_lines) - 1
            parsed_fragments.append(fragment)

        return parsed_fragments

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
        return words_in_line[0] in self.key_words

    def get_first_word_in_line(self, line):
        words = line.split()
        if len(words) == 0:
            return None
        return words[0]