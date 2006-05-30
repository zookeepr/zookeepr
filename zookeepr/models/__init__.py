import md5

from sqlalchemy import *

#import contentstor
from tables import *
#from forms import *

## Submission Types
class SubmissionType(object):
    def __init__(self, name=None):
        self.name = name

mapper(SubmissionType, submission_type)


## Submissions
class Submission(object):
    def __init__(self, title=None, submission_type=None, abstract=None, experience=None, url=None):
        self.title = title
        self.submission_type = submission_type
        self.abstract = abstract
        self.experience = experience
        self.url = url

mapper(Submission, submission,
       properties = dict(
    submission_type = relation(SubmissionType)
    ))


## Persons
class Person(object):
    def __init__(self, handle=None, email_address=None, password=None, firstname=None, lastname=None, phone=None, fax=None):
        self.handle = handle
        self.email_address = email_address

        if password is not None:
            self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.fax = fax

    def _set_password(self, password):
        self.password_hash = md5.new(password).hexdigest()

    def _get_password(self):
        return self.password_hash

    password = property(_get_password, _set_password)

# FIXME: hack to work around bug 191 in SQLAlchemy
class AccountMapperExtension(MapperExtension):
    def after_insert(self, mapper, connection, instance):
        for table in mapper.tables:
            if table.name == 'account':
                for col in mapper.pks_by_table[table]:
                    account_id = mapper._getattrbycolumn(instance, col)
                    break
        instance.account_id = account_id
        
mapper(Person, join(account, person), extension=AccountMapperExtension(),
       properties = dict(
    submissions = relation(Submission, private=True, backref='person')
    )
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

mapper(Registration, join(account, registration), extension=AccountMapperExtension())
