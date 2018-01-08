# docstrings2html
С помощью данной утилиты можно автоматически создавать документацию к модулям и пакетам Python! **Warning!** Если папка, в которую будет сохраняться документация, уже существует, то выбросится исключение.

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
- По ключу --exclude-special можно отфильтровать методы с двумя подчеркиваниями в начале. Например, __str__() или __special(). При этом, __init__ все ровно будет добавляться в документацию;
## Требования
- Python 3;
- [Yattag](http://www.yattag.org/) - библиотека для pythonic way генерации HTML и XML;

## Состав

- Логика работы утилиты: `architecture/`
- Css и js файлы для шаблона: `template/`
- Утилита для работы: `docstrings2html.py`
- Тесты: `tests/`

На многие модули(`architecture/*` кроме `html_builder.py`) написаны тесты, их можно найти в `/tests`. Покрытие по строкам составляет 89%

Для запуска тестов можно использовать `runtest.sh` (нужен `bash`, `coverage3`). 

```
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
architecture/__init__.py           0      0   100%
architecture/code_tree.py         54     11    80%   15-17, 32, 36-38, 43, 57-63, 66
architecture/docs_by_tree.py     128     40    69%   12-31, 39-65, 95, 100, 157, 161, 171, 174, 247, 254, 258-261
architecture/fragments.py         55      5    91%   17, 73-76
tests/test_code_tree.py           53      0   100%
tests/test_docs_by_tree.py       125      0   100%
tests/test_fragments.py           75      0   100%
------------------------------------------------------------
TOTAL                            490     56    89%
```

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
