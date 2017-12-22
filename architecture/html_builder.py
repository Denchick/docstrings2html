""" По построенной документации для кода формирует HTML-документ """

from yattag import Doc
from yattag import indent
from architecture.docs_by_tree import DocsByTree


class HtmlBuilder:

    def __init__(self, docs_by_tree):
        if not isinstance(docs_by_tree, DocsByTree):
            raise RuntimeError
        self.docs = docs_by_tree
        self.documentation_nodes = docs_by_tree.get_documentation_nodes()
        self.source_code = docs_by_tree.code
        self.module_description = docs_by_tree.module_description if docs_by_tree.module_description else 'no description'
        self.module_name = 'No-name module' if None else docs_by_tree.module_filename


    def get_html(self):
        """ должен возвращать сформированную html-документацию """
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html'):

            with tag('head'):
                doc.tag('meta', charset="utf-8")
                with tag('title'):
                    text('Documentation for {0}'.format(self.module_name))
                doc.stag('meta', name="viewport", content="width=device-width, initial-scale=1")
                doc.stag('meta', http_equiv="X-UA-Compatible", content="IE=edge")
                doc.stag('link', rel="stylesheet", href="cyborg.bootstrap.min.css", media="screen")
                doc.stag('link', rel="stylesheet", href="cyborg.bootstrap.css", media="screen")
                doc.stag('link', id="highlight-style", rel="stylesheet", href="default.css")
                doc.stag('link', rel="stylesheet", href="custom.min.css", media="screen")

            with tag('body'):
                with tag('nav', klass="navbar navbar-expand-lg fixed-top navbar-dark bg-dark"):
                    with tag('div', klass="container"):
                        with tag('a', klass="navbar-brand", href="https://github.com/Denchick/docstrings2html"):
                            text('docstring2html')

                        with tag('div', klass ="collapse navbar-collapse", id="navbarSupportedContent"):
                            with tag('ul', klass="nav navbar-nav ml-auto"):
                                with tag('li', klass="nav-item"):
                                    with tag('a', klass="nav-link", href="index.html"):
                                        text('Index')
                                with tag('li', klass="nav-item"):
                                    with tag('a', klass="nav-link", href="#source_code"):
                                        text('Source Code')
                                with tag('li', klass="nav-item"):
                                    with tag('a', klass="nav-link", href="#instance_methods"):
                                        text('Instance Methods')
                                with tag('li', klass="nav-item"):
                                    with tag('a', klass="nav-link", href="#method_details"):
                                        text('Method Details')
                with tag('div', klass='container'):

                    with tag('div', klass="page-header", id="banner"):
                        with tag('div', klass='row'):
                            with tag('div', klass="col-lg-8 col-md-7 col-sm-6"):
                                with tag('h1'):
                                    text(self.module_name)
                                with tag('p', klass="lead"):
                                    text(self.module_description if self.module_description else "Documentation for")

                    with tag('div', klass='col-lg-12'):

                        with tag('h2'):
                            text('Instance classes')
                        for m in self.docs.get_classes():
                            with tag('div', klass="jumbotron"):
                                with tag('h2'):
                                    text(m.signature)
                                with tag('p'):
                                    text(m.get_annotation() + '.')


                        if self.module_description:
                            with tag('p'):
                                text(self.module_description)
                        with tag('h2'):
                            text('Methods')
                        for m in self.docs.get_methods():
                            with tag('div', klass="jumbotron"):
                                with tag('h2'):
                                    text(m.get_name())
                                with tag('p'):
                                    with tag('code'):
                                        text(m.signature)
                                with tag('p'):
                                    text(m.get_annotation() + '.')

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
        with tag('script', src="highlight.pack.js"):
            text('')
        with tag('script'):
            text("hljs.initHighlightingOnLoad();")
        return indent(doc.getvalue())