

class Element:
    tag = 'html'

    def __init__ (self, content = None):
        self.content_input = []
        if content is not None:
            self.content_input.append(content)

    def append_text(self, content):
        self.content_input.append(content)

    def render(self, f, ind=""):
        start_tag = "<{}>".format(self.tag)
        f.write(start_tag)
        for text_line in self.content_input:
            try:
                text_line.render(f)
            except AttributeError:
                f.write(str(text_line))
        end_tag = "</{}>".format(self.tag)
        f.write(end_tag)


class Body(Element):
    tag = 'body'


class P(Element):
    tag = 'p'