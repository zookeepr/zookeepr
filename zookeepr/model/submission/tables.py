from sqlalchemy import *

# types of submissions: typically 'paper', 'miniconf', etc
submission_type = Table('submission_type',
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40),
                               unique=True,
                               nullable=False),
                        )

# submissions to the conference
submission = Table('submission', 
                   Column('id', Integer, primary_key=True),

                   # title of submission
                   Column('title', String()),
                   # abstract or description
                   Column('abstract', String()),
                   # attachment, if they've submitted a paper
                   Column('attachment', Binary()),

                   # type, enumerated in the submission_type table
                   Column('submission_type_id', Integer,
                          ForeignKey('submission_type.id')),

                   # their bio/experience presenting this topic
                   Column('experience', String()),

                   # url to a project page
                   Column('url', String()),

                   # do they need assistance?
                   Column('assistance', Boolean),
                   )

# for doing n-n mappings of people and submissions
person_submission_map = Table('person_submission_map',
    Column('person_id', Integer, ForeignKey('person.id'),
        nullable=False),
    Column('submission_id', Integer, ForeignKey('submission.id'),
        nullable=False),
    )
