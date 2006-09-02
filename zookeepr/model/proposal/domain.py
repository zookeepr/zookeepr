## Proposal Types
class ProposalType(object):
    def __init__(self, name=None):
        self.name = name

## Proposals
class Proposal(object):
    def __init__(self, id=None, title=None, type=None, abstract=None, experience=None, url=None, attachment=None):
        self.id = id
        self.title = title
        self.type = type
        self.abstract = abstract
        self.experience = experience
        self.url = url
        self.attachment = attachment

    def __repr__(self):
        return '<Proposal id="%r" title="%s">' % (self.id, self.title)

## Reviews
class Review(object):
    def __init__(self):
        pass

    def __repr__(self):
        return '<Review id=%d>' % (self.id,)
