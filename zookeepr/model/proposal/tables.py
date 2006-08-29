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
                   # attachment, if they've submitted a paper
                   Column('attachment', Binary()),

                   # type, enumerated in the proposal_type table
                   Column('proposal_type_id', Integer,
                          ForeignKey('proposal_type.id')),

                   # their bio/experience presenting this topic
                   Column('experience', String()),

                   # url to a project page
                   Column('url', String()),

                   # do they need assistance?
                   Column('assistance', Boolean),
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

                   Column('name', String,
                          nullable=False),
                   Column('content_type', String,
                          nullable=False),
                   
                   Column('creation_timestamp', DateTime,
                          nullable=False),

                   Column('content', Binary(),
                          nullable=False),

                   )
