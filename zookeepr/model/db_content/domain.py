class DBContentType(object):
    def __init__(self, name=None):
        self.name = name

class DBContent(object):
    def __init__(self,
                 title=None,
                 type=None,
                 urls=None,
                 body=None,
                 ):
        self.title = title
        self.type = type
        self.urls = urls
        self.body = body

