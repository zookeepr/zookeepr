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
    def __init__(self, proposal=None, reviewer=None, familiarity=None, technical=None, experience=None, coolness=None, stream=None, comment=None):
        self.proposal = proposal
        self.reviewer = reviewer
        self.familiarity = familiarity
        self.technical = technical
        self.experience = experience
        self.coolness = coolness
        self.stream = stream
        self.comment = comment

    def __repr__(self):
        return '<Review id=%d>' % (self.id,)
