## Submission Types
class SubmissionType(object):
    def __init__(self, name=None):
        self.name = name

## Submissions
class Submission(object):
    def __init__(self, id=None, title=None, submission_type_id=None, abstract=None, experience=None, url=None, attachment=None):
        self.id = id
        self.title = title
        self.submission_type_id = submission_type_id
        self.abstract = abstract
        self.experience = experience
        self.url = url
        self.attachment = attachment

    def __repr__(self):
        return '<Submission id="%r" title="%s">' % (self.id, self.title)
