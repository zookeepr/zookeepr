class Stream(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Stream name=%r>' % self.name

class Talk(object):
    """An accepted proposal, now in the programme.
    """

    def __repr__(self):
        return '<Talk id=%r>' % (self.id,)
