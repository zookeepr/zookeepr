## NOTE
##   If you plan on using SQLObject, the following should be un-commented and provides
##   a starting point for setting up your schema

#from sqlobject import *
#from pylons.database import PackageHub
#hub = PackageHub("zookeepr")
#__connection__ = hub

# You should then import your SQLObject classes
# from myclass import MyDataClass

import md5
import os.path

from sqlalchemy import *

person = Table('person',
               Column('id', Integer, primary_key=True),
               
               # unique identifier within the zookeepr app
               # useful for URLs
               Column('handle', String(40), unique=True),
               
               # login identifier and primary method of communicating
               # with person
               Column('email_address', String(512)),
               
               # password hash
               Column('password_hash', String(32)),

               # other personal details
               Column('firstname', String()),
               Column('lastname', String()),
               Column('phone', String()),
               Column('fax', String())
)

# types of submissions: typically 'paper', 'miniconf', etc
submission_type = Table('submission_type',
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40), unique=True)
                        )

# submissions to the conference
submission = Table('submission',
                   Column('id', Integer, primary_key=True),

                   # title of submission
                   Column('title', String()),
                   # abstract or description
                   Column('abstract', String()),

                   # type, enumerated in the submission_type table
                   Column('submission_type_id', Integer,
                          ForeignKey('submission_type.id')),

                   # person submitting
                   Column('person_id', Integer,
                          ForeignKey('person.id')),

                   # their bio/experience presenting this topic
                   Column('experience', String()),

                   # url to a project page
                   Column('url', String())
                   )

if not os.path.exists('somedb.db'):
    print "creating db"
    global_connect('sqlite', dict(filename='somedb.db'))
    person.create()
    submission_type.create()
    submission.create()
                  
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


# Use assign_mapper to monkeypatch the classes with useful methods
assign_mapper(SubmissionType, submission_type)

assign_mapper(Submission, submission, properties = dict(
    submission_type = relation(SubmissionType.mapper)
    ))

assign_mapper(Person, person, properties = dict(
    submissions = relation(Submission.mapper, private=True, backref='person')
    ))
