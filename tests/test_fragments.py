import struct
import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from architecture import fragments


class TestFragmentParser(unittest.TestCase):
    def test_correctParsing_whenNothingToParse(self):
        code_lines = []
        parse = fragments.FragmentsParser(code_lines)

        self.assertEqual(parse.parse_code_lines(), [])

    def test_correctParsing_whenOneEmptyLine(self):
        code_lines = ['']
        parse = fragments.FragmentsParser(code_lines)

        self.assertEqual(parse.parse_code_lines(), [])

    def test_correctParsing_whenOneNonEmptyLine(self):
        code_lines = ['just a string']
        parse = fragments.FragmentsParser(code_lines)

        self.assertEqual(parse.parse_code_lines(), [])

    def test_correctParsing_whenSeveralNonEmptyLines(self):
        code_lines = ['first string', 'second string', 'third string']
        parse = fragments.FragmentsParser(code_lines)

        self.assertEqual(parse.parse_code_lines(), [])

    def test_correctParsing_whenOneNonEmptyLine_withSpecialWord(self):
        code_lines = ['def smth line function']
        parse = fragments.FragmentsParser(code_lines)

        expected = [fragments.Fragment(0, 0, 'def', 0)]
        actual = parse.parse_code_lines()
        self.assertCountEqual(expected, actual)

    def test_correctParsing_whenSeveralLines_butNothingToParse(self):
        code_lines = [
            'line1 line1 line1 line1 line1',
            'line2 line2 line2 line2',
            'line3'
        ]
        parse = fragments.FragmentsParser(code_lines)

        expected = []
        actual = parse.parse_code_lines()
        self.assertCountEqual(expected, actual)

    def test_correctParsing_whenThereIsRealFunction(self):
        code_lines = [
            'def test:',
            '    this is = real',
            '    kek'
        ]
        parse = fragments.FragmentsParser(code_lines)

        expected = [fragments.Fragment(0, 2, 'def', 0)]
        actual = parse.parse_code_lines()
        self.assertCountEqual(expected, actual)

    def test_correctParsing_withTwoFragments(self):
        code_lines = [
            'def test:',
            '    this is = real',
            '    kek',
            'class kek:',
            '    pass'
        ]
        parse = fragments.FragmentsParser(code_lines)

        expected = [
            fragments.Fragment(0, 2, 'def', 0),
            fragments.Fragment(3, 4, 'class', 0)
        ]
        actual = parse.parse_code_lines()
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertTrue(i in actual)

    def test_correctParsing_withTwoFragments_separatedByEnter(self):
        code_lines = [
            'def test:',
            '    this is = real',
            '    kek',
            '',
            'class kek:',
            '    pass'
        ]
        parse = fragments.FragmentsParser(code_lines)

        expected = [
            fragments.Fragment(0, 3, 'def', 0),
            fragments.Fragment(4, 5, 'class', 0)
        ]
        actual = parse.parse_code_lines()
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertTrue(i in actual)

    def test_correctParsing_withTwoNestedFragments(self):
        code_lines = [
            'def test:',
            '    this is = real',
            '    kek',
            '    class kek:',
            '        pass'
        ]
        parse = fragments.FragmentsParser(code_lines)

        expected = [
            fragments.Fragment(0, 4, 'def', 0),
            fragments.Fragment(3, 4, 'class', 4)
        ]
        actual = parse.parse_code_lines()
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertTrue(i in actual)

    def test_correctParsing_withTwoNestedFragments_withEnter(self):
        code_lines = [
            'def test:',
            '    this is = real',
            '    kek',
            '',
            '    class kek:',
            '        pass'
        ]
        parse = fragments.FragmentsParser(code_lines)

        expected = [
            fragments.Fragment(4, 5, 'class', 4),
            fragments.Fragment(0, 5, 'def', 0)
        ]
        actual = parse.parse_code_lines()
        self.assertEqual(len(actual), len(expected))
        for i in actual:
            self.assertTrue(expected.__contains__(i))


if __name__ == "__main__":
    unittest.main()
