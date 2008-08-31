import datetime

## Proposal Types
class ProposalType(object):
    def __init__(self, name=None):
        self.name = name

## Assistance Types
class AssistanceType(object):
    def __init__(self, name=None):
        self.name = name

## Proposals
class Proposal(object):
    def __init__(self, id=None, title=None, type=None, assistance=None, abstract=None, url=None, attachment=None, code=None, scheduled=None, finished=None, theatre=None, building=None):
        self.id = id
        self.title = title
        self.type = type
        self.assistance = assistance
        self.abstract = abstract
        self.url = url
        self.attachment = attachment
        self.code = code
        self.scheduled = scheduled
        self.finished = finished
        self.theatre = theatre
        self.building = building

    def __repr__(self):
        return '<Proposal id="%r" title="%s">' % (self.id, self.title)


class Attachment(object):
    def __init__(self, filename=None, content_type=None, creation_timestamp=None, content=None):
        self.filename = filename
        self.content_type = content_type
        self.creation_timestamp = creation_timestamp
        self.content = content

    def _set_filename(self, value):
        if value is not None:
            self._filename = value
        else:
            self._filename = 'attachment'

    def _get_filename(self):
        return self._filename

    filename = property(_get_filename, _set_filename)

    def _set_content_type(self, value):
        if value is not None:
            self._content_type = value
        else:
            self._content_type = 'application/octet-stream'

    def _get_content_type(self):
        return self._content_type

    content_type = property(_get_content_type, _set_content_type)

    def __repr__(self):
        return '<Attachment id=%r filename="%s">' % (self.id, self.filename)


## Reviews
class Review(object):
    def __init__(self, proposal=None, reviewer=None, score=None, stream=None, comment=None):
        self.proposal = proposal
        self.reviewer = reviewer
        self.score = score
        self.stream = stream
        self.comment = comment

    def __repr__(self):
        return '<Review id=%r comment=%r>' % (self.id, self.comment)
