class Stream(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Stream name=%r>' % self.name
