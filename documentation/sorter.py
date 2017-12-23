#!/usr/bin/env python3
""" Внешняя сортировка """

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

try:
    from map_reduce import extremum, map_reduce, piece, utils
except Exception as e:
    print('Модули не найдены: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)

__version__ = '0.3'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'

LOGGER_NAME = 'sorter'
LOGGER = logging.getLogger(LOGGER_NAME)


def create_parser():
    """ Разбор аргументов командной строки """
    parser = argparse.ArgumentParser(
        description="""Внешняя сортировка файла, не помещающегося в оперативную память. Если не указывать файл, 
        то данные будут браться из sys.stdin.""")
    initialize_common_arguments(parser)

    subparsers = parser.add_subparsers(help='commands', dest='mode')
    create_number_subparser(subparsers)
    create_string_subparser(subparsers)
    create_csv_subparser(subparsers)

    return parser.parse_args()


def initialize_common_arguments(parser):
    parser.add_argument(
        '-f', '--filename', type=str,
        help='Файл, который необходимо отсортировать. По умолчанию данные берутся из stdin.')
    parser.add_argument(
        '-o', '--output', type=str,
        help='Название выхода - отсортированного файла. По умолчанию данные направлены в stdout.')
    parser.add_argument(
        '-t', '--temp', type=str,
        help='Название каталога для хранения временных файлов. По умолчанию временный каталог из модуля tempfile')
    parser.add_argument(
        '-p', '--piece', type=int,
        help='Примерное количество байт, которое можно использовать в оперативной памяти.')
    parser.add_argument(
        '-r', '--reverse', action='store_true', default=False, help='Сортировка в обратном порядке')
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False, help="""Режим debug. Временные файлы не удаляются. Warning! 
        В этом режиме папку с временными файлами необходимо удалять самостоятельно во избежание падения утилиты.""")


def create_number_subparser(subparsers):
    number_parser = subparsers.add_parser('numbers', help="Сортировка чисел")
    number_parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='Разделитель между значениями в исходном и отсортированном файле. По умолчанию перевод строки.')


def create_string_subparser(subparsers):
    string_parser = subparsers.add_parser('strings', help="Сортировка строк")
    string_parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='Разделитель между значениями в исходном и отсортированном файле. По умолчанию перевод строки.')
    string_parser.add_argument(
        '-c', '--case_sensitive', action='store_true', default=False, help='Регистрозависимая сортировка строк.')


def create_csv_subparser(subparsers):
    csv_parser = subparsers.add_parser('csv', help="Сортировка csv-таблицы по заданому столбцу")
    csv_parser.add_argument(
        '-c', '--column', type=int, default=1,
        help='Номер столбца, по которому нужно сортировать таблицу. Нумерация начинается с 1 слева-направо.')
    csv_parser.add_argument(
        '-dl', '--delimiter', type=str, default=',',
        help='Разделитель между значениями внутри csv-файла. По умолчанию запятая ",".')


def get_separator(args):
    if 'separator' in dir(args):
        return args.separator.encode().decode('unicode-escape')
    return '\n'


def main():
    args = create_parser()

    log = logging.StreamHandler(sys.stderr)
    log.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s <%(name)s>] %(message)s'))

    for module in (sys.modules[__name__], map_reduce):
        logger = logging.getLogger(module.LOGGER_NAME)
        logger.setLevel(logging.DEBUG if args.debug else logging.ERROR)
        logger.addHandler(log)

    print(type(args))

    map_reduce.MapReduce(
        input_filename=args.filename,
        output_filename=args.output,
        separator=get_separator(args),
        temp_directory=args.temp,
        size_of_one_piece=args.piece,
        case_sensitive=args.case_sensitive,
        reverse=args.reverse,
        debug=args.debug,
        **vars(args))


if __name__ == "__main__":
    main()
