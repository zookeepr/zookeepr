import md5

from sqlalchemy import *

import contentstor
from tables import *
from forms import *


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


class SubmissionType(object):
    def __init__(self, name=None):
        self.name = name


class Submission(object):
    def __init__(self, title, submission_type, abstract, experience, url):
        self.title = title
        self.submission_type = submission_type
        self.abstract = abstract
        self.experience = experience
        self.url = url


contentstor.modelise(SubmissionType, submission_type, SubmissionTypeSchema)

contentstor.modelise(Submission, submission, SubmissionSchema, dict(
    submission_type = relation(SubmissionType.mapper)
    ))

contentstor.modelise(Person, person, PersonSchema, properties = dict(
    submissions = relation(Submission.mapper, private=True, backref='person')
    ))

