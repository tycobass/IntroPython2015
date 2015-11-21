__author__ = 'Max'

"""
some simple tests for the html_render.py functions

designed to run with py.test or nose.
"""
import html_render as hr
from io import StringIO

def test_init():
    hr.Element()


def test_init2():
    hr.Element("test")


def test_content():
    e = hr.Element("this is a test")
    assert e.content is not None


def test_content_None():
    e = hr.Element()
    assert None not in e.content


def test_tag():
    e = hr.Element("this")
    assert hr.Element.tag == 'html'
    assert e.tag == 'html'


def test_append():
    e = hr.Element('this')
    e.append('that')
    assert 'that' in e.content
    assert 'this' in e.content


def test_render():
    e = hr.Element("this")
    e.append("that")
    f = StringIO()
    e.render(f)
    f.seek(0)
    text = f.read().strip() # Remove trailing white space
    assert text.startswith("<html>")
    assert text.endswith("</html>")
    assert "this" in text
    assert "that" in text


def test_body():
    e = hr.Body("this")
    f = StringIO()
    e.render(f)
    f.seek(0)
    text = f.read().strip() # Remove trailing white space
    assert text.startswith("<body>")
    assert text.endswith("</body>")
    assert "this" in text

def test_p():
    e = hr.P("this")
    f = StringIO()
    e.render(f)
    f.seek(0)
    text = f.read().strip() # Remove trailing white space
    assert text.startswith("<p>")
    assert text.endswith("</p>")
    assert "this" in text

def test_html():
    e = hr.Html("this")
    f = StringIO()
    e.render(f)
    f.seek(0)
    text = f.read().strip() # Remove trailing white space
    assert text.startswith("<html>")
    assert text.endswith("</html>")
    assert "this" in text


def test_next():
    e = hr.Element()
    p = hr.P("a paragraph of text")
    e.append(p)
    p = hr.P("another paragraph of text")
    e.append(p)
    f = StringIO()
    e.render(f)
    f.seek(0)
    text = f.read().strip()

    print(text)
    assert False


