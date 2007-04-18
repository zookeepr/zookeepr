import datetime

class Openday(object):
    def __init__(self,
                 firstname=None,
                 lastname=None,
                 email_address=None,
                 heardfrom=None,
                 heardfromtext=None,
                 opendaydrag=None,
                 ):
        self.firstname = firstname
        self.lastname = lastname
        self.email_address = email_address
        self.heardfrom = heardfrom
        self.heardfromtext = heardfromtext
        self.opendaydrag = opendaydrag

