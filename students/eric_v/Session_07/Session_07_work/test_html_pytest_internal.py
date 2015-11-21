

from io import StringIO

import html_render as hr


def test_init():
    hr.Element()


def test_init_text():
    hr.Element("some text")


def test_content_input():
    class_location = hr.Element('provide a little text')
    assert class_location.content_input is not None


def test_content_None():
    class_location = hr.Element('some trial text')
    print('my element list', class_location.content_input)
    assert None not in class_location.content_input


def test_content_str():
    class_location = hr.Element("this")
    print('my element list', class_location.content_input)
    assert "this" in class_location.content_input


def test_tag():
    class_location = hr.Element("this")
    assert hr.Element.tag == 'html'
    assert class_location.tag == 'html'


def test_append_text():
    class_location = hr.Element("this")
    class_location.append_text("that")
    assert 'that' in class_location.content_input
    assert 'this' in class_location.content_input


def test_render():
    class_location = hr.Element("this")
    class_location.append_text("that")
    f = StringIO()
    class_location.render(f)
    f.seek(0)
    text = f.read().strip()
    assert text.startswith("<html>")
    assert text.endswith("</html>")
    assert "this" in text
    assert "that" in text


def test_body():
    class_location = hr.Body("this")
    f = StringIO()
    class_location.render(f)
    f.seek(0)
    text = f.read().strip()
    assert text.startswith("<body>")
    assert text.endswith("</body>")
    assert "this" in text


def test_p():
    class_location = hr.P("this")
    f = StringIO()
    class_location.render(f)
    f.seek(0)
    text = f.read().strip()
    assert text.startswith("<p>")
    assert text.endswith("</p>")
    assert "this" in text


def test_nest():
    class_location = hr.Element()
    p = hr.P("a paragraph of text")
    class_location.append_text(p)
    p = hr.P("another paragraph of text")
    class_location.append_text(p)

    f = StringIO()
    class_location.render(f)
    f.seek(0)
    text = f.read().strip()
    print(text)

