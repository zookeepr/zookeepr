import datetime

class RegoNote(object):
    def __init__(self, note=None):
        self.note = note

    def __repr__(self):
        return '<RegoNote note=%r>' % (self.note)

class Volunteer(object):
    def __init__(self, areas=None, other=None, accepted=None):
        self.areas = areas
        self.other = other
        self.accepted = accepted

    def __repr__(self):
        return '<Volunteer id=%r person_id=%r>' % (self.id, self.person_id)
