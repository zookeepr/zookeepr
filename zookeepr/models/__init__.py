import datetime
import md5
import random

from sqlalchemy import mapper, relation, MapperExtension, join

#import contentstor
from zookeepr.models.tables import *
#from forms import *

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
                         ),
       )

## Submission Types
class SubmissionType(object):
    def __init__(self, name=None):
        self.name = name

mapper(SubmissionType, submission_type)


## Submissions
class Submission(object):
    def __init__(self, title=None, submission_type_id=None, abstract=None, experience=None, url=None, attachment=None):
        self.title = title
        self.submission_type_id = submission_type_id
        self.abstract = abstract
        self.experience = experience
        self.url = url
        self.attachment = attachment

mapper(Submission, submission,
       properties = dict(
    submission_type = relation(SubmissionType, lazy=False),
    person = relation(Person, lazy=False, backref='submissions')
    ))



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
    def __init__(self, timestamp=None, email_address=None, password=None, activated=None, fullname=None):
        self.timestamp = timestamp
        self.email_address = email_address
        self.password = password
        self.activated = activated
        self.fullname = fullname

        # url hash should never be modifiable by the caller directly
        self._update_url_hash()
        
    def _set_password(self, value):
        if value is not None:
            self.password_hash = md5.new(value).hexdigest()

    def _get_password(self):
        return self.password_hash

    password = property(_get_password, _set_password)

    def _set_timestamp(self, value):
        if value is None:
            self._timestamp = datetime.datetime.now()
        else:
            self._timestamp = value
        self._update_url_hash()

    def _get_timestamp(self):
        return self._timestamp

    timestamp = property(_get_timestamp, _set_timestamp)

    def _get_url_hash(self):
        return self._url_hash

    # Please note that url_hash can't be select_by()'d, instead you need to
    # select_by(_url_hash=...) (see the properties in the mapper below).  This
    # is ugly but is the recommended way to do this in SQLAlchemy.
    url_hash = property(_get_url_hash)
    
    def _update_url_hash(self):
        """Call this when an element of the url hash is changed
        (i.e. either set email address or timestamp)
        """
        nonce = random.randrange(0, 2**30)
        magic = "%s&%s&%s" % (self.email_address,
                              self.timestamp,
                              nonce)
        self._url_hash = md5.new(magic).hexdigest()

    def __repr__(self):
        return '<Registration email_address="%s" timestamp="%s" url_hash="%s" activated=%s>' % (self.email_address, self.timestamp, self.url_hash, self.activated)

    def _set_fullname(self, value):
        if value is not None:
            self.firstname = value.split(' ')[0]
            self.lastname = ' '.join(value.split(' ')[1:])
        else:
            self.firstname = None
            self.lastname = None

    def _get_fullname(self):
        r = self.firstname
        if self.lastname:
            r = r + ' ' + self.lastname
        return r

    fullname = property(_get_fullname, _set_fullname)

mapper(Registration, join(account, person).join(registration),
       properties = dict(account_id = [account.c.id, person.c.account_id, registration.c.account_id],
                         submissions = relation(Submission, lazy=True),
                         _url_hash = registration.c.url_hash,
                         )
       )

__all__ = ['Person', 'person', 'account']
