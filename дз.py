class Tag:
    def __init__(self, tag, is_single = False, toptier = False, klass = None, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.toptier = toptier
        self.attributt = {}
        self.text = ""
        self.children = []
        if klass is not None:
            self.attributt["class"] = " ".join(klass)
        for attr, val in kwargs.items():
            self.attributt[attr] = val
    def __enter__(self):
        return self
    def __exit__(self, *args):
        if self.toptier:
            print("<%s>"%self.tag)
            for child in self.children:
                print(child)
            print("</%s>"%self.tag)
    def __str__(self):
        attrs = []
        for attr, val in self.attributt.items():
            attrs.append("%s='%s'"%(attr, val))
        attrs = " ".join(attrs)
        if self.children:
            op = "<{tag} {attrs}>".format(tag = self.tag, attrs = attrs)
            inter = "%s"%self.text
            for child in self.children:
                inter += str(child)
            ed = "</%s>"%self.tag
            return op + inter + ed
        else:
            if self.is_single:
                return "<{tag} {attrs}>".format(tag = self.tag, attrs = attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(tag = self.tag, attrs = attrs, text = self.text)
    def __add__(self, other):
        self.children.append(other)
        return self
class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)

    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "\n</html>"
        return html
class TopLevelTag(Tag):
    def __init__(self, tag):
        self.is_single = False
        self.toptier = False
        self.tag = tag
        self.children = []
        self.attributt = {}
        self.text = ""
if __name__ == "__main__":
    with HTML(output = None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body
