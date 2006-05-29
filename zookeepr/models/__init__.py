import md5

from sqlalchemy import *

#import contentstor
from tables import *
#from forms import *

class Person(object):
    def __init__(self, handle=None, email_address=None, password=None, firstname=None, lastname=None, phone=None, fax=None):
        self.handle = handle
        self.email_address = email_address

        if password is not None:
            self.password_hash = md5.new(password).hexdigest()
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.fax = fax

    def _set_password(self, password):
        self.password_hash = md5.new(password).hexdigest()

    def _get_password(self, value):
        return self.password_hash

    password = property(_get_password, _set_password)

person_join = join(account, person)
mapper(Person, person_join)




# class SubmissionType(object):
#     def __init__(self, name=None):
#         self.name = name


# class Submission(object):
#     def __init__(self, title=None, submission_type=None, abstract=None, experience=None, url=None):
#         self.title = title
#         self.submission_type = submission_type
#         self.abstract = abstract
#         self.experience = experience
#         self.url = url


# contentstor.modelise(SubmissionType, submission_type, SubmissionTypeSchema)

# contentstor.modelise(Submission, submission, SubmissionSchema,
#                      properties = dict(
#     submission_type = relation(SubmissionType.mapper)
#     ))

# contentstor.modelise(Person, p_join, PersonSchema, properties = dict(
#     submissions = relation(Submission.mapper, private=True, backref='person')
#     ),
#                      primary_key = [person.c.id])

# class Role(object):
#     def __init__(self, name=None):
#         self.name = name

# contentstor.modelise(Role, role, RoleSchema, properties = dict(
#     people = relation(Person.mapper, person_role_map,
#                       lazy=False, backref='roles')
#     ))

# class Registration(object):
#     def __init__(self, timestamp=None, url_hash=None):
#         self.timestamp = timestamp
#         self.url_hash = url_hash

# contentstor.modelise(Registration, registration, None,
#                      properties = {
#     'person': relation(Person.mapper)
#     })

