

class Element:
    tag = 'html'

    def __init__(self, content:None):
        self.content = []
        if content is not None:
            self.content.append(content)

    def append(self, content):
        self.content.append(content)

    def render(self, f, ind " "):
        start_tag = "<{}>".format(self.tag)
        f.write(start_tag)
#        for s in self.content:
            f.write(" ".join(self.content))
        end_tag = "</{}>".format(self.tag)
        f.write(end_tag)

class Body(Element):
    tag = "body"

class P(Element):
    pass

