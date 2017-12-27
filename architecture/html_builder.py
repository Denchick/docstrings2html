""" По построенной документации для кода формирует HTML-документ """
import os
from yattag import Doc
from yattag import indent
from architecture.docs_by_tree import DocsByTree


class HtmlBuilder:

    def __init__(self, docs_by_tree, path_to_root, path_to_template_root):
        if not isinstance(docs_by_tree, DocsByTree):
            raise RuntimeError
        self.docs = docs_by_tree
        self.path_to_root = path_to_root
        self.path_to_template_root = path_to_template_root
        self.documentation_nodes = docs_by_tree.get_documentation_nodes()
        self.source_code = docs_by_tree.code
        self.module_description = docs_by_tree.module_description
        self.module_name = 'No-name module' if None else docs_by_tree.module_filename

    @staticmethod
    def get_path_to_source(path, source_name):
        if source_name.endswith('css'):
            return '{0}/css/{1}'.format(path, source_name)
        if source_name.endswith('js'):
            return '{0}/js/{1}'.format(path, source_name)
        return '{0}/{1}'.format(path, source_name)

    def get_html(self):
        """ Возвращать сформированную html-документацию для одного модуля"""
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html'):

            with tag('head'):
                doc.tag('meta', charset="utf-8")
                with tag('title'):
                    text('Documentation for {0}'.format(self.module_name))
                doc.stag('meta', name="viewport", content="width=device-width, initial-scale=1")
                doc.stag('meta', http_equiv="X-UA-Compatible", content="IE=edge")
                doc.stag('meta', charset="utf-8")
                doc.stag('link', rel="stylesheet", href=self.get_path_to_source(self.path_to_template_root, "cyborg.bootstrap.min.css"), media="screen")
                doc.stag('link', rel="stylesheet", href=self.get_path_to_source(self.path_to_template_root, "cyborg.bootstrap.css"), media="screen")
                doc.stag('link', id="highlight-style", rel="stylesheet", href=self.get_path_to_source(self.path_to_template_root, "default.css"))
                doc.stag('link', rel="stylesheet", href=self.get_path_to_source(self.path_to_template_root, "custom.min.css"), media="screen")

            with tag('body'):
                # Navigation
                with tag('nav', klass="navbar navbar-expand-lg fixed-top navbar-dark bg-dark"):
                    with tag('div', klass="container"):
                        with tag('a', klass="navbar-brand", href="https://github.com/Denchick/docstrings2html"):
                            text('docstrings2html')

                        with tag('div', klass ="collapse navbar-collapse", id="navbarSupportedContent"):
                            with tag('ul', klass="nav navbar-nav ml-auto"):
                                with tag('li', klass="nav-item"):
                                    with tag('a', klass="nav-link", href=os.path.join(self.path_to_root, 'index.html')):
                                        text('Start page')
                                with tag('li', klass="nav-item"):
                                    with tag('a', klass="nav-link", href="index.html"):
                                        text('Index')
                                with tag('li', klass="nav-item"):
                                    with tag('a', klass="nav-link", href="#source_code"):
                                        text('Source Code')
                                with tag('li', klass="nav-item"):
                                    with tag('a', klass="nav-link", href="#instance_classes"):
                                        text('Instance Classes')
                                with tag('li', klass="nav-item"):
                                    with tag('a', klass="nav-link", href="#methods"):
                                        text('Methods')

                with tag('div', klass='container'):

                    # Header
                    with tag('div', klass="page-header", id="banner"):
                        with tag('div', klass='row'):
                            with tag('div', klass="col-lg-8 col-md-7 col-sm-6"):
                                with tag('h1'):
                                    text(self.module_name)
                                with tag('p', klass="lead"):
                                    text(self.module_description if self.module_description else "Documentation for")

                    #Content
                    with tag('div', klass='col-lg-12'):

                        if self.module_description:
                            with tag('p'):
                                text(self.module_description)

                        with tag('h2'):
                            with tag('a', name="instance_classes"):
                                text('Instance Classes')
                        for m in self.docs.get_classes():
                            with tag('div', klass="jumbotron"):
                                with tag('h2'):
                                    text(m.signature)
                                with tag('p'):
                                    text(m.get_annotation() + '.')

                        with tag('h2'):
                            with tag('a', name="methods"):
                                text('Methods')
                        for m in self.docs.get_methods():
                            with tag('div', klass="jumbotron"):
                                with tag('h2'):
                                    text(m.get_name())
                                with tag('p'):
                                    with tag('code'):
                                        text(m.signature)
                                with tag('pre', klass="description"):
                                    text(m.get_docstring())

                    #Source code
                    with tag('h2'):
                        with tag('a', name="source_code"):
                            text('Source code')
                    with tag('pre'):
                        with tag('code', klass="py"):
                            text(self.source_code)

                    with tag('footer', id="footer"):
                        with tag('div', klass="row"):
                            with tag('div', klass="col-lg-12"):
                                with tag('ul', klass="list-unstyled"):
                                    with tag('li', klass="float-lg-right"):
                                        with tag('a', href="#top"):
                                            text('Back to top')
        with tag('script', src=self.get_path_to_source(self.path_to_template_root, "highlight.pack.js")):
            text('')
        with tag('script'):
            text("hljs.initHighlightingOnLoad();")
        return indent(doc.getvalue())

    @staticmethod
    def get_index_page_html(path_to_template_root, files):
        """ Возвращать сформированную html-документацию для одного модуля"""
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('head'):
                doc.tag('meta', charset="utf-8")
                with tag('title'):
                    text('Documentation for {0}'.format(path_to_template_root))
                doc.stag('meta', name="viewport", content="width=device-width, initial-scale=1")
                doc.stag('meta', http_equiv="X-UA-Compatible", content="IE=edge")
                doc.stag('meta', charset="utf-8")
                doc.stag('link', rel="stylesheet", href=HtmlBuilder.get_path_to_source(path_to_template_root, "cyborg.bootstrap.min.css"), media="screen")
                doc.stag('link', rel="stylesheet", href=HtmlBuilder.get_path_to_source(path_to_template_root, "cyborg.bootstrap.css"), media="screen")
                doc.stag('link', rel="stylesheet", href=HtmlBuilder.get_path_to_source(path_to_template_root, "custom.min.css"), media="screen")

            with tag('body'):
                # Navigation
                with tag('nav', klass="navbar navbar-expand-lg fixed-top navbar-dark bg-dark"):
                    with tag('div', klass="container"):
                        with tag('a', klass="navbar-brand", href="https://github.com/Denchick/docstrings2html"):
                            text('docstrings2html')

                        with tag('div', klass="collapse navbar-collapse", id="navbarSupportedContent"):
                            with tag('ul', klass="nav navbar-nav ml-auto"):
                                with tag('li', klass="nav-item"):
                                    with tag('a', klass="nav-link", href="index.html"):
                                        text('Index')
                with tag('div', klass='container'):
                    # Content
                    with tag('div', klass='bs-docs-section'):
                        with tag('div', klass="jumbotron"):
                            with tag('ul'):
                                for f in files:
                                    with tag('li'):
                                        with tag('a', href=f if f.endswith('html') else '{0}/index.html'.format(f)):
                                            text(f)

                    with tag('footer', id="footer"):
                        with tag('div', klass="row"):
                            with tag('div', klass="col-lg-12"):
                                with tag('ul', klass="list-unstyled"):
                                    with tag('li', klass="float-lg-right"):
                                        with tag('a', href="#top"):
                                            text('Back to top')

        return indent(doc.getvalue())