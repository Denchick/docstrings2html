# docstrings2html
С помощью данной утилиты можно автоматически создавать документацию к модулям и пакетам Python!

Версия 1.0

Автор: Волков Денис (denchick1997@mail.ru)

## Что уже умеет

- По отдельному файлу строить HTML-документацию;
- По нескольким файлам строить HTML-документацию;
- Строить документацию по пакету;
- Все файлы хранятся в отдельном каталоге, который можно указать;
- Каждый файл связан с другими разными ссылками, то есть есть неплохая навигация по документации;
- Для отображения всех HTML-файлов используется один шаблон, написанный с использованием веб-фреймворка Bootstrap;
- Внутри каждого HTML-файла указаны относительные пути до папки с CSS и JS файлами;
- Исходный код можно также передать на `stdin`, тогда в качестве результата на `stdout` будет просто выведен сгенерированный HTML-код;
- На основную логику работы программы (парсинг кода, постройка дерева) есть тесты. Много тестов;
- Работает одинаково хорошо как под Windows, так и под Linux;

## Требования
- Python 3;
- [Yattag](http://www.yattag.org/) - библиотека для pythonic way генерации HTML и XML;

## Состав

- Логика работы утилиты: `architecture/`
- Css и js файлы для шаблона: `template/`
- Утилита для работы: `docstrings2html.py`
- Тесты: `tests/`

Для запуска тестов можно использовать `runtest.sh` (нужен `bash`, `coverage3`).

## Как это работает

На вход утилите подается исходный файл или несколько файлов, или пакет.
Каждый файл с кодом на питоне (`*.py`) разбивается на фрагменты (модуль `architecture/fragments.py`). Они могут вложенные, идти друг за другом и так далее (но не пересекаются).

Далее, по этим фрагментам строится дерево (модуль `architecture/code_tree.py`). Таким образом легко определить, какие классы и функции вложены друг в друга.

После этого, по построенному дереву код еще раз анализируется, и для каждой функции и класса записываются потомки, запоминаются docstrings и некоторая другая информация (модуль `architecture/docs_by_tree.py`).

В конце, собранная информация по модулю генерируется в HTML-код(модули `architecture/html_builder.py`). При работе с HTML используется веб-фреймворк Bootstrap и пакет Yattag для Python.

В самом конце копируется структура директорий проекта, а в соответствующих директориях, на месте модулей, сохраняются html-файлы (модуль `architecture/linker.py`), каждый файл описывает строго один модуль. В каждой директории создается index.html, в котором записывается, какие модули есть в данной директории.

## Запуск

Справка по запуску: `./docstring2html.py --help`

Пример запуска:
`
./docstrings2html.py -f test_file1.py test_file2.py
`