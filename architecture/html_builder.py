""" По построенной документации для кода формирует HTML-документ """

from yattag import Doc
from yattag import indent
from architecture.docs_by_tree import DocsByTree


class HtmlBuilder:

    def __init__(self, docs_by_tree):
        if not isinstance(docs_by_tree, DocsByTree):
            raise RuntimeError
        self.docs = docs_by_tree

    def get_html(self):
        """ должен возвращать сформированную html-документацию """
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html'):

            with tag('head'):
                doc.tag('meta', charset="utf-8")
                with tag('title'):
                    text('Bootswatch: Cyborg')
                doc.tag('meta', name="viewport", content="width=device-width, initial-scale=1")
                doc.stag('meta', http_equiv="X-UA-Compatible", content="IE=edge")
                doc.tag('link', rel="stylesheet", href="../4/cyborg/bootstrap.css", media="screen")

            with tag('body'):
                with tag('div', klass='container'):
                    with tag('div', klass='row'):
                        text('Hello world!')

        print(indent(doc.getvalue()))








