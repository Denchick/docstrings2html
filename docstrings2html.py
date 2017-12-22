#!/usr/bin/env python3
""" Перевод python docstrings в HTML формат """
from architecture import code_tree
from architecture.code_tree import CodeTree
from architecture.docs_by_tree import DocsByTree
from architecture.html_builder import HtmlBuilder

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
    pass
except Exception as e:
    print('Модули не найдены: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)

__version__ = '0.0'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'

LOGGER_NAME = 'docstrings2html'
LOGGER = logging.getLogger(LOGGER_NAME)


def create_parser():
    """ Разбор аргументов командной строки """
    parser = argparse.ArgumentParser(
        description="""Создает HTML-документацию для модуля или файла в файле в текущей директории.""")
    parser.add_argument(
        'filename', type=str,
        help="""Путь до файла.""")
    parser.add_argument(
        '-o', '--output', type=str,
        help="""Название файла.""")
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help="""Режим debug.""")
    parser.add_argument(
        '--version', action='store_true', default=False,
        help="Печатает версию утилиты и выходит.")

    return parser.parse_args()


def main():
    args = create_parser()

    if args.version:
        print(__version__)
        sys.exit()

    log = logging.StreamHandler(sys.stderr)
    log.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s <%(name)s>] %(message)s'))

    logger = logging.getLogger(sys.modules[__name__].LOGGER_NAME)
    logger.setLevel(logging.DEBUG if args.debug else logging.ERROR)
    logger.addHandler(log)

    builder(args.filename)


def get_code(code_filename):
    with open(code_filename, 'r', encoding='utf-8') as f:
        return f.read()


def builder(code_filename):
    code = get_code(code_filename)
    code_lines = code.split('\n')
    tree = CodeTree(code_lines)
    docs = DocsByTree(tree, code_lines, code, code_filename)
    html_obj = HtmlBuilder(docs)

    out = html_obj.get_html()
    print(out)
    with open(r'C:\Users\Volkov\YandexDisk\Python_курс\docstrings2html\themes\index.html', 'w') as f:
        f.write(out)

if __name__ == "__main__":
    main()