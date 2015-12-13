#   test_html.py
#   most of the comments here are for my own benefit

#   import the file html_render as "hr", for shorthand
import html_render as hr
#   import StringIO
#   StringIO prepares what amounts to a text file in memory, so we don't have to worry about making, writng/reading to/from an actual text file
from io import StringIO

def render_me(element):
    """ a utility to render an elment so you can see if its doing the right thing """
  
    f = StringIO()
    #    refering back to the the element argument in the function, we test the render function within hr with the imaginary string created from StringIO
    element.render(f)
    #   when looking at the given file, .seek (0) returns us to the beginning of it
    f.seek(0)
    #   return the given file
    return f.read()
#   test whether the class Element is even there
def test_init():
    hr.Element()
#   test whether Element contains anything    
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
    e = hr.Element('this')
    print(e.content)
    assert 'this' in e.content

def test_tag():
    e = hr.Element('this')
    assert hr.Element.tag == 'html'
    assert e.tag == 'html'

def test_append():
    e = hr.Element('this')
    e.append('that')
    assert 'that' in e.content
    assert 'this' in e.content

def test_render():
    render_me(element)
    e = hr.Element('this')
    e.append('that')
   
    text = f.read().strip()
    assert text.startswith('<html>')
    assert text.endswith('</html>') 
    assert "this" in text
    assert "that" in text
    print(text)
    assert False

def head_test():
    render_me(element)

def test_body():
    render_me(element)
    e = hr.Body('this')
    
    text = f.read().strip()
    assert text.startswith('<body>')
    assert text.endswith('</body>') 
    assert 'this' in test

def test_P():
    e = hr.Body('this')
    render_me(element)
    text = f.read().strip()
    assert text.startswith('<p>')
    assert text.endswith('</p>') 
    assert 'this' in test

def test_nest():
    e = hr.Element()
    p = hr.P('a paragraph')
    e.append(p)
    render_me(element)
    text = f.read().strip()
    assert text.startswith('<p>')
    assert text.endswith('</p>') 
    assert 'this' in test
    
    print (text)
    assert False


def test_indent():
    render_me(element)
    
def test_Title():
    render_me(element)

def test_OneLineTag():
    render_me(element)

def test_Title_OneLineTag():
    render_me(element)
