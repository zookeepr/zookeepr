import os.path

from sqlalchemy import *

person = Table('person',
               Column('id', Integer, primary_key=True),
               
               # secondary key, unique identifier within the zookeepr app
               # useful for URLs
               Column('handle', String(40), unique=True, nullable=False),
               
               # login identifier and primary method of communicating
               # with person
               Column('email_address', String(512), unique=True),
               
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


if os.path.exists('somedb.db'):
    # we do this inside the 'if' because global_connect on an sqlite
    # db creates the file
    global_connect('sqlite', dict(filename='somedb.db'))
else:    
    print "creating db"
    global_connect('sqlite', dict(filename='somedb.db'))
    person.create()
    submission_type.create()
    submission.create()
