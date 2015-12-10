from io import StringIO
import html_render as hr

def test_init():
    hr.Element()

def test_init2():
    hr.Element("some text")

def test_content():
    e = hr.Element("some_text")
    assert e.content is not None