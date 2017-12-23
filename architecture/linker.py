
from architecture.code_tree import CodeTree
from architecture.docs_by_tree import DocsByTree
from architecture.html_builder import HtmlBuilder
import shutil, os, sys

class Linker:

    def __init__(self, path, args):

        if self.check_input_is_a_packet(args):
            self.copy_source_directory(args[0], path)
            self.copy_template_folders(path)
            exit()
            for filename in self.walk_through_files(path):
                print(filename)
            exit()
            for filename in args:
                source_code = self.get_source_code(filename)
                html = self.get_html_code(source_code, filename)
                self.save_generated_file(os.path.join(path, '{0}.html'.format(filename)), html)

        elif self.ckeck_input_is_a_stdin(args):
            source_code = self.get_source_code(None)
            html = self.get_html_code(source_code, None)
            self.save_generated_file(None, html)

        else:
            self.copy_template_folders(path)
            for filename in args:
                source_code = self.get_source_code(filename)
                html = self.get_html_code(source_code, filename)
                self.save_generated_file(os.path.join(path, '{0}.html'.format(filename)), html)

    def check_input_is_a_packet(self, args):
        return args and len(args) == 1 and os.path.isdir(args[0])

    def ckeck_input_is_a_stdin(self, *args):
        return args is None

    def copy_template_folders(self, path):
        shutil.copytree('./template', os.path.join(path, 'template'))

    def get_source_code(self, filename):
        with open(filename, 'r', encoding='utf-8') if filename else sys.stdin as f:
            return f.read()

    def walk_through_files(self, path, file_extension='.py'):
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                if filename.endswith(file_extension):
                    yield os.path.join(dirpath, filename)

    def save_generated_file(self, filename, html):
        with open(filename, 'w') if filename else sys.stdout as f:
            f.write(html)

    def get_html_code(self, source_code, filename):
        code_lines = source_code.split('\n')
        tree = CodeTree(code_lines)
        docs = DocsByTree(tree, code_lines, source_code, filename)
        html_obj = HtmlBuilder(docs, '')
        return html_obj.get_html()

    def copy_source_directory(self, source, destination):
        shutil.copytree(source, destination, ignore=include_only_function('.py'))


def ignore_function(ignore):
    def _ignore_(path, names):
        ignored_names = []
        if ignore in names:
            ignored_names.append(ignore)
        return set(ignored_names)
    return _ignore_

def include_only_function(*includes):
    def _ignore_(path, names):
        ignored_names = []
        for name in names:
            for include in includes:
                if not name.endswith(include) and '.' in name or name == '__pycache__':
                    ignored_names.append(name)
        return set(ignored_names)
    return _ignore_