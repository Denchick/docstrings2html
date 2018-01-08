#!/usr/bin/env python3
""" Генератор случайных значений """

ERROR_EXCEPTION = 1
ERROR_WRONG_SETTINGS = 2
ERROR_PYTHON_VERSION = 3
ERROR_MODULES_MISSING = 4

import sys

if sys.version_info < (3, 0):
    print('Используйте Python версии 3.0 и выше', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

import argparse
import logging
import re

try:
    from generators import numbers_generator, strings_generator
except Exception as e:
    print('Модули не найдены: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)

__version__ = '2.0'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'

LOGGER_NAME = 'generator'
LOGGER = LOGGER = logging.getLogger(LOGGER_NAME)


def parse_range(range_as_string):
    """ Парсит строку с диапапазоном генерируемых значений """
    m = re.match(r'\((-?\d+),(-?\d+)\)$', range_as_string)
    if not m:
        raise ValueError('"{0}" не диапазон значений'.format(range_as_string))
    a, b = int(m.group(1)), int(m.group(2))
    if a <= 0 or b <= 0:
        raise ValueError('Длина строки не может иметь не положительную длину: {}'
                         .format(min(a, b)))
    return min(a, b), max(a, b)


def write_to_file(list_data, separator, filename):
    """ Записывает данные в файл filename через разделитель separator.
    Если filename == None, то вывод направляется в stdout
    """
    with open(filename, 'w') if filename else sys.stdout as output:
        data = separator.join(list_data)
        output.write(data)


def generate_list_data(args):
    """ По аргументам определяет, какой режим программы выбран и запускает генераторы. 
    Возвращается список строк - сгенерированные значения """
    if 'lowercase' in dir(args):
        return strings_generator.StringGenerator(args.digits, args.uppercase, args.lowercase,
                                                 args.special, args.count, args.range).generate()
    return numbers_generator.NumberGenerator(args.count, args.range).generate()


def create_parser():
    description = """Генератор случайных значений. 
    По умолчанию генерирует 10 строк, состоящих из цифр, прописных и заглавных букв английского алфавита,
    разделенных переносом строки."""
    parser = argparse.ArgumentParser(
        description=description)

    parser.add_argument(
        '-o', '--output', type=str, help='Имя выходного файла. По умолчанию выход направлен в stdout.')
    parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='Разделитель между значениями. По умолчанию перевод строки - \\n.')
    parser.add_argument(
        '-c', '--count', type=int, default=10,
        help='Количество генерируемых значений. По умолчанию 10.')
    parser.add_argument(
        '-d', '--debug',
        action='store_true', help='Режим debug.', default=False)

    subparsers = parser.add_subparsers(help='commands')
    create_number_subparser(subparsers)
    create_string_subparser(subparsers)

    return parser.parse_args()


def create_number_subparser(subparsers):
    number_parser = subparsers.add_parser('numbers', help="Генарация чисел")
    number_parser.add_argument(
        '-r', '--range', type=parse_range, default=(-100, 100),
        help="""Диапазон генерируемых чисел в формате (leftBorder, rightBorder). Границы включаются. 
        По умолчанию (-100,100).""")


def create_string_subparser(subparsers):
    string_parser = subparsers.add_parser('strings', help="Генерация строк")
    string_parser.add_argument(
        '-r', '--range', type=parse_range, default=(-100, 100),
        help="""Диапазон длин генерируемых строк в формате (leftBorder, rightBorder). Границы включаются. 
        По умолчанию (-100,100).""")
    string_parser.add_argument(
        '-di', '--digits',
        action='store_true', help='В алфавите генерации есть цифры.', default=False)
    string_parser.add_argument(
        '-up', '--uppercase',
        action='store_true', help='В алфавите генерации есть прописные буквы.', default=False)
    string_parser.add_argument(
        '-lo', '--lowercase',
        action='store_true', help='В алфавите генерации есть строчные буквы.', default=False)
    string_parser.add_argument(
        '-sp', '--special',
        action='store_true', help='В алфавите генерации есть специальные символы из string.punctuation.', default=False)


def main():
    args = create_parser()

    log = logging.StreamHandler(sys.stderr)
    log.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s <%(name)s>] %(message)s'))
    for module in (sys.modules[__name__], strings_generator, numbers_generator):
        logger = logging.getLogger(module.LOGGER_NAME)
        logger.setLevel(logging.DEBUG if args.debug else logging.ERROR)
        logger.addHandler(log)

    LOGGER.info('Application is start.')

    write_to_file(generate_list_data(args), args.separator, args.output)


if __name__ == "__main__":
    main()
