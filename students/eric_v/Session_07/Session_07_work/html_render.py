

class Element:
    tag = 'html'

    def __init__ (self, content = None):
        self.content_input = []
        if content is not None:
            self.content_input.append(content)

    def append_text(self, content):
        self.content_input.append(content)

    def render(self, file_output, ind=""):
        start_tag = "<{}>".format(self.tag)
        file_output.write(start_tag)
        for text_line in self.content_input:
            try:
                text_line.render(file_output)
            except AttributeError:
                file_output.write(str(text_line))
        end_tag = "</{}>".format(self.tag)
        file_output.write(end_tag)


class Body(Element):
    tag = 'body'


class P(Element):
    tag = 'p'