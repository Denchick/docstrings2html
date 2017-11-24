import struct
import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from architecture import fragments_parser
from architecture import code_fragment


class TestFragmentParser(unittest.TestCase):
    def test_correct_parsing_when_nothing_to_parse(self):
        codeLines = []
        parse = fragments_parser.Parser(codeLines)

        self.assertEqual(parse.parse_code_hierarchy(0), [])

    def test_correct_parsing_when_one_empty_line(self):
        codeLines = ['']
        parse = fragments_parser.Parser(codeLines)

        self.assertEqual(parse.parse_code_hierarchy(0), [])

    def test_correct_parsing_when_one_non_empty_line(self):
        codeLines = ['just a string']
        parse = fragments_parser.Parser(codeLines)

        self.assertEqual(parse.parse_code_hierarchy(0), [])

    def test_correct_parsing_when_several_non_empty_lines(self):
        codeLines = ['first string', 'second string', 'third string']
        parse = fragments_parser.Parser(codeLines)

        self.assertEqual(parse.parse_code_hierarchy(0), [])

    def test_correct_parsing_when_one_non_empty_line_with_special_word(self):
        codeLines = ['def smth line function']
        parse = fragments_parser.Parser(codeLines)

        expected = [code_fragment.CodeFragment(0, 0, 'def', 0)]
        actual = parse.parse_code_hierarchy(0)
        self.assertCountEqual(expected, actual)

    def test_correct_parsing_when_several_lines_but_nothing_to_parse(self):
        codeLines = [
            'line1 line1 line1 line1 line1',
            'line2 line2 line2 line2',
            'line3'
        ]
        parse = fragments_parser.Parser(codeLines)

        expected = []
        actual = parse.parse_code_hierarchy(0)
        self.assertCountEqual(expected, actual)

    def test_correct_parsing_when_there_is_real_function(self):
        codeLines = [
            'def test:',
            '    this is = real',
            '    kek'
        ]
        parse = fragments_parser.Parser(codeLines)

        expected = [code_fragment.CodeFragment(0, 2, 'def', 0)]
        actual = parse.parse_code_hierarchy(0)
        self.assertCountEqual(expected, actual)

    def test_correct_parsing_with_two_fragments(self):
        codeLines = [
            'def test:',
            '    this is = real',
            '    kek',
            'class kek:',
            '    pass'
        ]
        parse = fragments_parser.Parser(codeLines)

        expected = [
            code_fragment.CodeFragment(0, 2, 'def', 0),
            code_fragment.CodeFragment(3, 4, 'class', 0)
        ]
        actual = parse.parse_code_hierarchy(0)
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertTrue(i in actual)

    def test_correct_parsing_with_two_fragments_separated_by_enter(self):
        codeLines = [
            'def test:',
            '    this is = real',
            '    kek',
            '',
            'class kek:',
            '    pass'
        ]
        parse = fragments_parser.Parser(codeLines)

        expected = [
            code_fragment.CodeFragment(0, 3, 'def', 0),
            code_fragment.CodeFragment(4, 5, 'class', 0)
        ]
        actual = parse.parse_code_hierarchy(0)
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertTrue(i in actual)

    def test_correct_parsing_with_two_nested_fragments(self):
        codeLines = [
            'def test:',
            '    this is = real',
            '    kek',
            '    class kek:',
            '        pass'
        ]
        parse = fragments_parser.Parser(codeLines)

        expected = [
            code_fragment.CodeFragment(0, 4, 'def', 0),
            code_fragment.CodeFragment(3, 4, 'class', 4)
        ]
        actual = parse.parse_code_hierarchy(0)
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertTrue(i in actual)

    def test_correct_parsing_with_two_nested_fragments_with_enter(self):
        codeLines = [
            'def test:',
            '    this is = real',
            '    kek',
            '',
            '    class kek:',
            '        pass'
        ]
        parse = fragments_parser.Parser(codeLines)

        expected = [
            code_fragment.CodeFragment(4, 5, 'class', 4),
            code_fragment.CodeFragment(0, 5, 'def', 0)
        ]
        actual = parse.parse_code_hierarchy(0)
        self.assertEqual(len(actual), len(expected))
        for i in actual:
            self.assertTrue(expected.__contains__(i))


if __name__ == "__main__":
    unittest.main()