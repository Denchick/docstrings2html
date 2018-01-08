from architecture import utils
from architecture.code_tree import CodeTree
from architecture.docs_by_tree import DocsByTree
from architecture.html_builder import HtmlBuilder
import shutil
import os


class Linker:
    def __init__(self, path, exclude_special, files):
        """  """
        self.template_directory = 'template'
        self.exclude_special = exclude_special
        if self.check_input_is_a_packet(files):
            self.copy_source_directory(files[0], path)
            self.copy_template_directory(path, self.template_directory)

            for filename in utils.walk_through_files(path):
                source_code = utils.get_text_from_file(filename)
                joined = os.path.join(path, self.template_directory)
                relpath_to_template = os.path.relpath(joined, filename)[3:]
                html = self.get_module_html_code(source_code,
                                                 filename,
                                                 '',
                                                 relpath_to_template)
                utils.write_to_file('{0}.html'.format(filename[:-3]), html)
                os.remove(filename)
            self.create_index_pages(path)

        elif self.ckeck_input_is_a_stdin(files):
            source_code = utils.get_text_from_file(None)
            html_code = self.get_module_html_code(source_code, '', '', '')
            utils.write_to_file(None, html_code)

        else:
            self.copy_template_directory(path, self.template_directory)
            for filename in files:
                source_code = utils.get_text_from_file(filename)
                html = self.get_module_html_code(source_code,
                                                 filename,
                                                 '',
                                                 self.template_directory)
                joined = os.path.join(path, '{0}.html'.format(filename[:-3]))
                utils.write_to_file(joined, html)
            self.create_index_pages(path)

    @staticmethod
    def copy_template_directory(path, template_directory):
        copy_from = './{0}'.format(template_directory)
        copy_to = os.path.join(path, template_directory)
        shutil.copytree(copy_from, copy_to)

    def check_input_is_a_packet(self, files):
        return files and len(files) == 1 and os.path.isdir(files[0])

    def ckeck_input_is_a_stdin(self, files):
        return not files

    def get_module_html_code(self,
                             source_code,
                             filename,
                             path_to_root,
                             path_to_template):
        code_lines = source_code.split('\n')
        tree = CodeTree(code_lines)
        docs = DocsByTree(tree, code_lines, source_code, filename)
        self.html_builder = HtmlBuilder(docs, path_to_root, path_to_template)
        return self.html_builder.get_html()

    def copy_source_directory(self, source, destination):
        shutil.copytree(source,
                        destination,
                        ignore=utils.include_only_function('.py'))

    def create_index_pages(self, path):
        for dirpath in utils.walk_through_directories(path):
            if self.template_directory in dirpath:
                continue
            dirs = os.listdir(dirpath)
            if dirpath == path:
                dirs.remove(self.template_directory)
            joined = os.path.join(path, self.template_directory)
            relative_path_to_template = os.path.relpath(joined, dirpath)
            html = self.html_builder.get_index_page_html(
                relative_path_to_template,
                dirs)
            utils.write_to_file(os.path.join(dirpath, 'index.html'), html)
