import os
import sys


def ignore_function(ignore):
    """ Ignore function for shutil.copytree.  """
    def _ignore_(path, names):
        ignored_names = []
        if ignore in names:
            ignored_names.append(ignore)
        return set(ignored_names)
    return _ignore_


def include_only_function(*includes):
    """ Ignore all except *include files extensions,
    non-hidded folders and __pycache__.
     Use for shutil.copytree """
    def _ignore_(path, names):
        ignored_names = []
        for name in names:
            for include in includes:
                if not name.endswith(include) and '.' in name or '__' in name:
                    ignored_names.append(name)
        return set(ignored_names)
    return _ignore_


def get_text_from_file(filename):
    with open(filename, 'r', encoding='utf-8') if filename else sys.stdin as f:
        return f.read()


def walk_through_files(path, file_extension='.py'):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith(file_extension):
                yield os.path.join(dirpath, filename)


def walk_through_directories(path):
    yield path
    for (dirpath, dirnames, filenames) in os.walk(path):
        for dirname in dirnames:
            yield os.path.join(dirpath, dirname)


def write_to_file(filename, text):
    with open(filename, 'w', encoding='utf-8') if filename else sys.stdout as f:
        f.write(text)
