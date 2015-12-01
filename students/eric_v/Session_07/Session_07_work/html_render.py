

class Element:
    tag = 'html'
    indent = 4

    def __init__ (self, content = None):
        self.content_input = []
        if content is not None:
            self.content_input.append(content)

    def append_text(self, content):
        self.content_input.append(content)

    def render(self, file_output, ind=""):
        start_tag = "<{}>".format(self.tag)
        file_output.write(start_tag)
        file_output.write('\n'+(self.indent*" "))
        for text_line in self.content_input:
            try:
                text_line.render(file_output)
            except AttributeError:
                file_output.write(str(text_line))
        file_output.write('\n')
        end_tag = "</{}>".format(self.tag)
        file_output.write(end_tag)
        file_output.write('\n')


class Head(Element):
    tag = 'head'


class Title(Element):
    tag = 'title'


class Body(Element):
    tag = 'body'


class LI(Element):
    tag = 'li'


class A(Element):
    tag = 'a'


class P(Element):
    tag = 'p'
