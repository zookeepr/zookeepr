## NOTE
##   If you plan on using SQLObject, the following should be un-commented and provides
##   a starting point for setting up your schema

#from sqlobject import *
#from pylons.database import PackageHub
#hub = PackageHub("zookeepr")
#__connection__ = hub

# You should then import your SQLObject classes
# from myclass import MyDataClass

import os

from sqlalchemy import *

try:
    os.unlink('somedb.db')
except OSError:
    pass

snuh_engine = create_engine('sqlite', dict(filename='somedb.db'))

person = Table('person', snuh_engine,
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
               Column('phone', String())
)

submission_types = Table('submission_type', snuh_engine,
                         Column('id', Integer, primary_key=True),
                         Column('name', String(40), unique=True)
                         )

submission = Table('submission', snuh_engine,
                   Column('id', Integer, primary_key=True),
                   Column('title', String()),
                   Column('submission_type_id', Integer,
                          ForeignKey('submission_type.id')),
                   Column('abstract', String()),
                   Column('person_id', Integer,
                          ForeignKey('person.id')),
                   Column('experience', String()),
                   Column('url', String())
                   )

person.create()
submission_types.create()
submission.create()

class SubType(object):
    def __init__(self, name):
        self.name = name


class Person(object):
    def __init__(self, handle):
        self.handle = handle

class Submission(object):
    def __init__(self, title, submission_type, abstract, experience, url):
        self.title = title
        self.submission_type = submission_type
        self.abstract = abstract
        self.experience = experience
        self.url = url


SubType.mapper = mapper(SubType, submission_types)
Submission.mapper = mapper(Submission, submission, properties = {
    'submission_type': relation(SubType.mapper)
    }
                           )
Person.mapper = mapper(Person, person, properties = {
    'submissions': relation(Submission.mapper, private=True, backref='person')
    }
                       )

#jaq = Person('jaq', 'jaq@spacepants.org', 'snuh')
#
#paper = SubType('Paper')
#SubType("Rock")
#SubType("scissors")
#
#submission = Submission('sub 1', paper, 'bleh', 'poo', 'h://')
#
#jaq.submissions.append(Submission('foo', paper, 'bar', 'sod', 'http://'))
#
#objectstore.commit()
#
#print jaq.submissions[0].title
#
#print jaq.submissions[0].person.handle

