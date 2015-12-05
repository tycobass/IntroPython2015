
class Element:
    tag = 'html'
    attributes = ''
    indentation_spaces = '    '

    def __init__(self, content=None):
        self.content = []
        if content is not None:
            self.content.append(content)

    def __init__(self, *args, **kwargs):
        self.content = []

        for i in args:
            self.content.append(i)

        for n in kwargs:
            if len(self.attributes) > 0:
                self.attributes += ", "
            else:
                self.attributes = " "   # start with a space
            self.attributes += "{}=\"{}\"".format(n, kwargs[n])

    def render(self, f, ind=""):
        start_tag = "{}<{}{}>{}".format(ind, self.tag, self.attributes, '')
        f.write(start_tag)

        for el in self.content:

            try:
                if isinstance(el, Element):
                    f.write('\n')
                # if this is an Element object, this method will succeed
                el.render(f, ind+self.indentation_spaces)
            except AttributeError:
                f.write("{}{}{}".format('\n',
                        ind+self.indentation_spaces,
                        str(el)))

        end_tag = "{}{}</{}>".format('\n', ind, self.tag)
        f.write(end_tag)

    def append(self, content):
        self.content.append(content)


class Body(Element):
    tag = 'body'


class P(Element):
    tag = 'p'


class Html(Element):
    tag = 'html'

    def __init__(self, *args, **kwargs):
        self.content = []

        for i in args:
            self.content.append(i)

        for n in kwargs:
            if len(self.attributes) > 0:
                self.attributes += ", "
            else:
                self.attributes = " "  # start with a space
            self.attributes += "{}=\"{}\"".format(n, kwargs[n])

    def render(self, f, ind=""):
        # this line below is the different between the Element's method
        # and the Html class's method.
        f.write("{}{}".format('<!DOCTYPE html>\n',
                ind+self.indentation_spaces))
        start_tag = "{}<{}{}>{}".format(ind, self.tag, self.attributes, '')
        f.write(start_tag)

        ind = '    '

        for el in self.content:

            try:
                if isinstance(el, Element):
                    f.write('\n')
                # if this is an Element object, this method will succeed
                el.render(f, ind+self.indentation_spaces)
            except AttributeError:
                f.write("{}{}{}".format('\n',
                        ind+self.indentation_spaces,
                        str(el)))

        end_tag = "{}{}</{}>".format('\n', ind, self.tag)
        f.write(end_tag)


class Head(Element):
    tag = 'head'


class OneLineTag(Element):
    tag = 'one-line-tag'

    def render(self, f, ind=""):

        if len(self.content) == 0:
            start_tag = "{}<{} ".format(ind, self.tag)
        else:
            start_tag = "{}<{}{}>{}".format(ind, self.tag, self.attributes, '')

        f.write(start_tag)
        for el in self.content:

            try:
                if isinstance(el, Element):
                    f.write('')
                # if this is an Element object, this method will succeed
                el.render(f, ind+self.indentation_spaces)
            except AttributeError:
                f.write("{}".format(str(el)))

        # for s in self.content:
        # f.write(s)
        # f.write(" ".join(self.content))
        if len(self.content) == 0:
            end_tag = "/>"
        else:
            end_tag = "{}{}</{}>".format('', '', self.tag)

        f.write(end_tag)


class Title(OneLineTag):
    tag = 'title'


class Hr(OneLineTag):
    tag = 'hr'


class H(OneLineTag):
    tag = ''

    def __init__(self, *args, **kwargs):
        self.content = []
        assert len(args) == 2, "Expected two arguments for H tag"

        self.content.append(args[1])
        self.tag = "h{}".format(str(args[0]))


class A (OneLineTag):
    tag = 'a'

    def __init__(self, *args, **kwargs):
        self.content = []
        assert len(args) == 2, "Expected two arguments for A tag"

        self.content.append(args[1])
        self.attributes = " {}=\"{}\"".format('href', args[0])


class Ul(Element):
    tag = 'ul'

    def __init__(self, *args, **kwargs):
        self.content = []

        for i in args:
            self.content.append(i)

        for n in kwargs:
            if len(self.attributes) > 0:
                self.attributes += " "
            else:
                self.attributes = " "  # start with a space
            self.attributes += "{}=\"{}\"".format(n, kwargs[n])


class Li(Element):
    tag = 'li'


class Meta(OneLineTag):
    tag = 'meta'

    def render(self, f, ind=""):
        assert len(self.content) == 0, "Meta expects no content to be present"
        start_tag = "{}<{}{} ".format(ind, self.tag, self.attributes)

        f.write(start_tag)

        for el in self.content:

            try:
                if isinstance(el, Element):
                    f.write('')
                # if this is an Element object, this method will succeed
                el.render(f, ind+self.indentation_spaces)
            except AttributeError:
                f.write("{}".format(str(el)))

        end_tag = "/>"

        f.write(end_tag)
