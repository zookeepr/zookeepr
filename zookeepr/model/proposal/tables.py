import sqlalchemy.mods.threadlocal
from sqlalchemy import *

# types of proposals: typically 'paper', 'miniconf', etc
proposal_type = Table('proposal_type',
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40),
                               unique=True,
                               nullable=False),
                        )

# proposals to the conference
proposal = Table('proposal', 
                   Column('id', Integer, primary_key=True),

                   # title of proposal
                   Column('title', String()),
                   # abstract or description
                   Column('abstract', String()),

                   # type, enumerated in the proposal_type table
                   Column('proposal_type_id', Integer,
                          ForeignKey('proposal_type.id')),

                   # their bio/experience presenting this topic
                   Column('experience', String()),

                   # url to a project page
                   Column('url', String()),

                   # do they need assistance?
                   Column('assistance', Boolean),

                 # Is it accepted?
                 Column('accepted', Boolean),

                 Column('creation_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp()),
                 Column('last_modification_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp(),
                        onupdate=func.current_timestamp()),
                   )

# for doing n-n mappings of people and proposals
person_proposal_map = Table('person_proposal_map',
    Column('person_id', Integer, ForeignKey('person.id'),
        nullable=False),
    Column('proposal_id', Integer, ForeignKey('proposal.id'),
        nullable=False),
    )

# for storing attachments
attachment = Table('attachment',
                   Column('id', Integer, primary_key=True),

                   Column('proposal_id', Integer, ForeignKey('proposal.id')),

                   Column('filename', String,
                          key='_filename',
                          nullable=False),
                   Column('content_type', String,
                          key='_content_type',
                          nullable=False),
                   
                   Column('creation_timestamp', DateTime,
                          nullable=False,
                          default=func.current_timestamp()),
                   Column('last_modification_timestamp', DateTime,
                          nullable=False,
                          default=func.current_timestamp(),
                          onupdate=func.current_timestamp()),

                   Column('content', Binary(),
                          nullable=False),

                   )

# reviews of proposals
review = Table('review',
               Column('id', Integer, primary_key=True),

               Column('proposal_id', Integer,
                      ForeignKey('proposal.id'),
                      nullable=False,
                      ),
               Column('reviewer_id', Integer,
                      ForeignKey('person.id'),
                      nullable=False,
                      ),
               UniqueConstraint('proposal_id', 'reviewer_id', name='ux_review_proposal_reviewer'),

               Column('familiarity', Integer),
               Column('technical', Integer),
               Column('experience', Integer),
               Column('coolness', Integer),

               Column('stream_id', Integer,
                      ForeignKey('stream.id'),
                      ),
               Column('comment', String),

               Column('creation_timestamp', DateTime,
                      nullable=False,
                      default=func.current_timestamp()),
               Column('last_modification_timestamp', DateTime,
                      nullable=False,
                      default=func.current_timestamp(),
                      onupdate=func.current_timestamp()),

               )
