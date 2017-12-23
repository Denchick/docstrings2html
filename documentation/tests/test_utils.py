import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from map_reduce import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.filename = 'temp.txt'

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_get_next_data_piece(self):
        def pattern_for_testing_without_exceptions(data, separator, count, expected):
            with open(self.filename, 'w') as f:
                f.write(separator.join(data))
            with open(self.filename, 'r') as f:
                result = utils.get_next_data_piece(f, count, separator)
                self.assertEqual(result, expected)

        def pattern_for_testing_with_exceptions(data, separator, count, error_type):
            sep = ';' if not isinstance(separator, str) else separator
            with open(self.filename, 'w') as f:
                f.write(sep.join(data))
            with open(self.filename, 'r') as f:
                with self.assertRaises(error_type):
                    utils.get_next_data_piece(f, count, separator)

        pattern_for_testing_without_exceptions(['kek', 'cheburek'], ';', 3, 'kek')
        pattern_for_testing_without_exceptions(['kek', 'cheburek'], ';', 4, 'kek')
        pattern_for_testing_without_exceptions(['kek', 'cheburek'], ';', 5, 'kek;cheburek')
        pattern_for_testing_without_exceptions(['kek'], ';', 4, 'kek')
        pattern_for_testing_without_exceptions(['kek', 'cheburek'], ';', 20, 'kek;cheburek')

        pattern_for_testing_with_exceptions(['kek'], ';', '401', TypeError)
        pattern_for_testing_with_exceptions(['kek'], True, 2, TypeError)
        with self.assertRaises(AttributeError):
            utils.get_next_data_piece('not_file', 10, '\n')


if __name__ == "__main__":
    unittest.main()
