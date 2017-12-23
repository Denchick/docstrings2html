import unittest
import os
import sys
import shutil

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from map_reduce import piece


class TestPiece(unittest.TestCase):
    def setUp(self):
        self.directory = 'temp'
        os.mkdir(self.directory)

    def tearDown(self):
        shutil.rmtree(self.directory, ignore_errors=False, onerror=None)

    def test_init(self):
        with self.assertRaises(TypeError):
            piece.Piece('not_number', '', '')
        with self.assertRaises(TypeError):
            piece.Piece(1, ['not_string'], '')
        with self.assertRaises(TypeError):
            piece.Piece(1, 'kek', 123)
        with self.assertRaises(AttributeError):
            piece.Piece(1, 'kek', 'directory_is_definitely_not_exists')

        with self.assertRaises(AttributeError):
            with open('just_file', 'w') as f:
                piece.Piece(1, 'kek', 'just_file')
        os.remove('just_file')

    def test_write_to_filename(self):
        data = '\n'.join(['first', 'second', 'third'])
        p = piece.Piece(0, data, self.directory)
        p.write_to_filename(data, self.directory)
        self.assertEqual(data, p.get_data(self.directory))

    def test_get_data(self):
        p = piece.Piece(0, '', self.directory)
        self.assertEqual(p.get_data(self.directory), '')

        data = '\n'.join(['first', 'second', 'third'])
        p = piece.Piece(1, data, self.directory)
        self.assertEqual(p.get_data(self.directory), data)
        p.move_data_pointer(100)
        self.assertEqual(p.get_data(self.directory), data)

    def test_get_up_element(self):
        separator = '\n'
        data = separator.join(['first', 'second', 'third'])
        p = piece.Piece(1, data, self.directory)
        self.assertEqual(p.get_up_element(self.directory, separator), 'first')
        p.move_data_pointer(1)
        self.assertEqual(p.get_up_element(self.directory, separator), 'irst')
        p.move_data_pointer(4)
        self.assertEqual(p.get_up_element(self.directory, separator), 'second')
        p.move_data_pointer(1)
        self.assertEqual(p.get_up_element(self.directory, separator), 'second')

    def test_move_data_pointer(self):
        data = '\n'.join(['first', 'second', 'third'])
        p = piece.Piece(0, data, self.directory)

        with self.assertRaises(TypeError):
            p.move_data_pointer(None)
        with self.assertRaises(RuntimeError):
            p.move_data_pointer(-1 - p.data_pointer)

        p.move_data_pointer(2)
        self.assertEqual(p.data_pointer, 2)
        p.move_data_pointer(2)
        self.assertEqual(p.data_pointer, 4)
        p.move_data_pointer(100)
        self.assertEqual(p.data_pointer, 104)

    def test_is_empty(self):
        data = 'kek cheburek'

        # Так как только создали объект, то файл не пуст
        p = piece.Piece(2, data, self.directory)
        self.assertFalse(p.is_empty(self.directory))

        # Даже если его полностью прочитать, он не должен быть пустым
        p.get_data(self.directory)
        self.assertFalse(p.is_empty(self.directory))

        # get_up_element не должен смещать каретку, эти 2 вызова возвращают
        # один и тот же элемент - 'kek'
        p.get_up_element(self.directory, ' ')
        p.get_up_element(self.directory, ' ')
        self.assertFalse(p.is_empty(self.directory))

        # сместим data_pointer на 4, должен вернуть cheburek
        p.move_data_pointer(4)
        p.is_empty(self.directory)


if __name__ == "__main__":
    unittest.main()
