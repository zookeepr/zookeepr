from sqlalchemy import *

from zookeepr.model import metadata


# types of assistance:
assistance_type = Table('assistance_type', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40),
                               unique=True,
                               nullable=False),
                        )


# proposals to the conference
                        default=func.current_timestamp(),
                        onupdate=func.current_timestamp()),
                        # onupdate should really use
                        #   func.current_timestamp()
                        # but the version of sqlalchemy on the server can't
                        # cope with that, saying something about
                        # timezones...
                   )

# for doing n-n mappings of people and proposals
person_proposal_map = Table('person_proposal_map', metadata,
    Column('person_id', Integer, ForeignKey('person.id'),
        nullable=False),
    Column('proposal_id', Integer, ForeignKey('proposal.id'),
        nullable=False),
    )

# for storing attachments
attachment = Table('attachment', metadata,
                   Column('id', Integer, primary_key=True),

                   Column('proposal_id', Integer, ForeignKey('proposal.id')),

                   Column('filename', Text,
                          key='_filename',
                          nullable=False),
                   Column('content_type', Text,
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
review = Table('review', metadata,
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

               Column('score', Integer),

               Column('stream_id', Integer,
                      ForeignKey('stream.id'),
                      ),
               Column('miniconf', Text),
               Column('comment', Text),

               Column('creation_timestamp', DateTime,
                      nullable=False,
                      default=func.current_timestamp()),
               Column('last_modification_timestamp', DateTime,
                      nullable=False,
                      default=func.current_timestamp(),
                      onupdate=func.current_timestamp()),
                      # onupdate should really use
                      #   func.current_timestamp()
                      # but the version of sqlalchemy on the server can't
                      # cope with that, saying something about
                      # timezones...
               )
