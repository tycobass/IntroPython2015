

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


def test_head():
    class_location = hr.Head("my_head")
    f = StringIO()
    class_location.render(f)
    f.seek(0)
    text = f.read().strip()
    assert text.startswith("<head>")
    assert text.endswith("</head>")
    assert "my_head" in text


def test_body():
    class_location = hr.Body("rabbits ate my lunch")
    f = StringIO()
    class_location.render(f)
    f.seek(0)
    text = f.read().strip()
    assert text.startswith("<body>")
    assert text.endswith("</body>")
    assert "rabbits" in text


def test_p():
    class_location = hr.P("another paragraph")
    f = StringIO()
    class_location.render(f)
    f.seek(0)
    text = f.read().strip()
    assert text.startswith("<p>")
    assert text.endswith("</p>")
    assert "paragraph" in text


def test_head_section():
    class_location = hr.Element()
    head = hr.Head("a header section")
    class_location.append_text(head)
    title = hr.Title("a title section")
    class_location.append_text(title)
    f = StringIO()
    class_location.render(f)
    f.seek(0)
    text = f.read().strip()
    print(text)



def test_nest_b():
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


def test_indent():
    p = hr.P('a little text')
    f = StringIO()
    p.render(f)
    f.seek(0)
    text = f.read()
    assert text == """<p>
    a little text
</p>
"""


def test_indent():
    p = hr.P('a little text - 4 spaces')
    f = StringIO()
    p.render(f)
    f.seek(0)
    text = f.read()
    assert text == """<p>
    a little text
</p>
"""


def test_additional_indent():
    p = hr.P('a little text - 8 spaces')
    p.indent = 8
    f = StringIO()
    p.render(f)
    f.seek(0)
    text = f.read()
    assert text == """<p>
        a little text
</p>
"""
