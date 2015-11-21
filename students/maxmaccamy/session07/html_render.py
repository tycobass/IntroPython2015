__author__ = 'Max'

class Element:
    tag = "html"
    indent = ""

    def __init__(self, content = None):
        self.content = []
        if (content is not None):
            self.content.append(content)

    def append(self, newContent):
        self.content.append(newContent)

    def render(self, file_out, ind = ""):
        file_out.write("<{}>\n".format(self.tag))
        for el in self.content:
            try:
                el.render(file_out)
            except(AttributeError):
                file_out.write(str(el) + "\n")
        file_out.write("</{}>\n".format(self.tag))

class Html(Element):
    tag = 'html'

    def __init__(self, content = None):
        self.content = []
        if (content is not None):
           self.content.append(content)


class Body(Element):
    tag = 'body'
    def __init__(self, content = None):
        self.content = []
        if (content is not None):
            self.content.append(content)


class P(Element):
    tag = 'p'
    def __init__(self, content = None):
        self.content = []
        if (content is not None):
            self.content.append(content)