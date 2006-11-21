import datetime

class InvoiceItem(object):
    def __init__(self, description=None, cost=None):
        self.description = description
        self.cost = cost

    def __repr__(self):
        return '<InvoiceItem id=%r description=%r cost=%r>' % (self.id, self.description, self.cost)

class Invoice(object):
    def __init__(self, issue_date=None):
        self.issue_date = issue_date

    def __repr__(self):
        return '<Invoice id=%r person=%r>' % (self.id, self.person_id)
