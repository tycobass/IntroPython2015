from io import StringIO
import html_render as hr

def test_init():
    hr.Element()


def test_init2():
    hr.Element("some text")


def test_content():
    e = hr.Element("some text")
    assert e.content is not None


def test_content_None():
    e = hr.Element()
    print(e.content)
    assert None not in e.content


def test_content_str():
    e = hr.Element("this")
    print(e.content)
    assert "this" in e.content


def test_tag():
    e = hr.Element("this")
    assert e.tag == 'html'


def test_append():
    e = hr.Element("this")
    e.append("that")
    assert 'this' in e.content
    assert 'that' in e.content


def test_render():
    e = hr.Element("this")
    e.append("that")
    f = StringIO()
    e.render(f)
    f.seek(0)
    text = f.read()
    assert text.startswith("<html>")
    assert text.endswith("</html>")
    assert "this" in text
    assert "that" in text
    print(text)

def test_nest():
    e = hr.Element()
    p = hr.p("paragraph")
    e.append(p)
    f.seek(0)
    text = f.read().strip()
    print(text)
