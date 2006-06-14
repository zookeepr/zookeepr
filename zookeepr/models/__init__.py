import md5

from sqlalchemy import mapper, relation, MapperExtension, join

#import contentstor
from zookeepr.models.tables import *
#from forms import *

## Submission Types
class SubmissionType(object):
    def __init__(self, name=None):
        self.name = name

mapper(SubmissionType, submission_type)


## Submissions
class Submission(object):
    def __init__(self, title=None, submission_type=None, abstract=None, experience=None, url=None, attachment=None):
        self.title = title
        self.submission_type = submission_type
        self.abstract = abstract
        self.experience = experience
        self.url = url
        self.attachment = attachment

mapper(Submission, submission,
       properties = dict(
    submission_type = relation(SubmissionType)
    ))


## Persons
class Person(object):
    def __init__(self, handle=None, email_address=None, password=None,
                 firstname=None, lastname=None, phone=None, fax=None):

        self.handle = handle
        self.email_address = email_address

        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.fax = fax

    def get_unique(self):
        if self.handle:
            return self.handle
        else:
            return self.id

    def _set_password(self, password):
        if password is None:
            self.password_hash = None
        else:
            self.password_hash = md5.new(password).hexdigest()

    def _get_password(self):
        return self.password_hash

    password = property(_get_password, _set_password)

    def __repr__(self):
        return "<Person id=%s handle=%s>" % (self.id, self.handle)


mapper(Person, join(account, person),
       properties = dict(account_id = [account.c.id, person.c.account_id],
                         submissions = relation(Submission,
                                                private=True,
                                                backref='person')
                         ),
       )

class Role(object):
    def __init__(self, name=None):
        self.name = name

mapper(Role, role, properties = dict(
    people = relation(Person,
                      secondary=person_role_map,
                      lazy=False,
                      backref='roles')
    ))

class Registration(object):
     def __init__(self, timestamp=None, url_hash=None, email_address=None, password=None):
         self.timestamp = timestamp
         self.url_hash = url_hash
         self.email_address = email_address
         self.password = password

     def _set_password(self, value):
         self.password_hash = md5.new(value).hexdigest()

     def _get_password(self):
         return self.password_hash

     password = property(_get_password, _set_password)

mapper(Registration, join(account, registration),
       properties = dict(account_id = [account.c.id, registration.c.account_id])
       )

class CFP(object):
    def __init__(self, email_address=None, password=None, handle=None, firstname=None, lastname=None, title=None, abstract=None, type=None, experience=None, url=None, attachment=None):
        self.email_address = email_address
        self.password = password
        self.handle = handle
        self.firstname = firstname
        self.lastname = lastname
        self.title = title
        self.abstract = abstract
        self.type = type
        self.experience = experience
        self.url = url
        self.attachment = attachment

    def _set_password(self, password):
        if password is None:
            self.password_hash = None
        else:
            self.password_hash = md5.new(password).hexdigest()

    def _get_password(self):
        return self.password_hash

    password = property(_get_password, _set_password)

mapper(CFP, join(account, person).join(submission),
       properties = {
    'account_id': [account.c.id, person.c.account_id],
    'person_id': [person.c.id, submission.c.person_id],
    'type': submission.c.submission_type_id,
    }
       )

__all__ = ['Person', 'person', 'account']
