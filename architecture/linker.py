from architecture import utils
from architecture.code_tree import CodeTree
from architecture.docs_by_tree import DocsByTree
from architecture.html_builder import HtmlBuilder
import shutil, os, sys

class Linker:

    def __init__(self, path, args):
        """  """
        self.template_directory = 'template'
        if self.check_input_is_a_packet(args):
            self.copy_source_directory(args[0], path)
            shutil.copytree('./{0}'.format(self.template_directory), os.path.join(path, self.template_directory))
            for filename in utils.walk_through_files(path):
                source_code = utils.get_text_from_file(filename)
                html = self.get_module_html_code(source_code, filename, '', os.path.relpath(os.path.join(path, self.template_directory), filename)[3:])
                utils.write_to_file('{0}.html'.format(filename[:-3]), html)
                os.remove(filename)
            self.create_index_pages(path)

        elif self.ckeck_input_is_a_stdin(args):
            source_code = utils.get_text_from_file(None)
            html = self.get_module_html_code(source_code, None)
            utils.write_to_file(None, html)

        else:
            shutil.copytree('./{0}'.format(self.template_directory), os.path.join(path, self.template_directory))
            for filename in args:
                source_code = utils.get_text_from_file(filename)
                html = self.get_module_html_code(source_code, filename, '')
                utils.write_to_file(os.path.join(path, '{0}.html'.format(filename)), html)
            self.create_index_pages(path)

    def check_input_is_a_packet(self, args):
        return args and len(args) == 1 and os.path.isdir(args[0])

    def ckeck_input_is_a_stdin(self, *args):
        return args is None

    def get_module_html_code(self, source_code, filename, path_to_root, path_to_template):
        code_lines = source_code.split('\n')
        tree = CodeTree(code_lines)
        docs = DocsByTree(tree, code_lines, source_code, filename)
        self.html_builder = HtmlBuilder(docs, path_to_root, path_to_template)
        return self.html_builder.get_html()

    def copy_source_directory(self, source, destination):
        shutil.copytree(source, destination, ignore=utils.include_only_function('.py'))

    def create_index_pages(self, path):
        for dirpath in utils.walk_through_directories(path):
            if dirpath.endswith(self.template_directory):
                continue
            dirs = os.listdir(dirpath)
            if dirpath == path:
                dirs.remove(self.template_directory)
            relative_path_to_template = os.path.relpath(os.path.join(path, self.template_directory), dirpath)
            html = self.html_builder.get_index_page_html(relative_path_to_template, dirs)
            utils.write_to_file(os.path.join(dirpath, 'index.html'), html)