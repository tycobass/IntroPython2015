
#import StringIO
#holds stuff in memory--don't need to list out
class Element:
    tag = 'html'

    def __init__(self,content=None):

#need a list to hold your data, but you have to put the list in self
        self.content = []
        if content is not None:
            self.content.append(content)

    def append(self, content):
        self.content.append(content)


    def render(self, f, ind=""):
        start_tag = "<{}>".format(self.tag)
        f.write(start_tag)
        for el in self.contents:
            el.render(f)
#            f.write(" ".join(self.content))
        end_tag = "</{}>".format(self.tag)
        f.write(end_tag)

class Body(Element):
    tag = 'body'
#need to get each object to render itself

class P(Body):
    tag = 'p'