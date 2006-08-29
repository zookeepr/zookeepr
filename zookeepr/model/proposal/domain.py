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


class Attachment(object):
    def __init__(self, name=None, content_type=None, creation_timestamp=None, content=None):
        self.name = name
        self.content_type = content_type
        self.creation_timestamp = creation_timestamp
        self.content = content

    def __repr__(self):
        return '<Attachment id="%r" name="%s">' % (self.id, self.name)
