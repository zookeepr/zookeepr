from sqlalchemy import *

from zookeepr.model import metadata

# types of proposals: typically 'paper', 'miniconf', etc
proposal_type = Table('proposal_type', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40),
                               unique=True,
                               nullable=False),
                        )

# types of assistance: 
assistance_type = Table('assistance_type', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40),
                               unique=True,
                               nullable=False),
                        )


# proposals to the conference
proposal = Table('proposal', metadata,
                   Column('id', Integer, primary_key=True),

                   # title of proposal
                   Column('title', Text),
                   # abstract or description
                   Column('abstract', Text),

                   # type, enumerated in the proposal_type table
                   Column('proposal_type_id', Integer,
                          ForeignKey('proposal_type.id')),

                   # type, enumerated in the assistance_type table
                   Column('assistance_type_id', Integer,
                          ForeignKey('assistance_type.id')),

                   # name and url of the project
                   Column('project', Text),
                   Column('url', Text),

                   # url to a short video
                   Column('abstract_video_url', Text),

                   # Is it accepted?
                   Column('accepted', Boolean),

                   Column('code', Integer),
                   Column('scheduled', DateTime),
                   Column('finished', DateTime),
                   Column('theatre', Text),
                   Column('building', Text),

                   Column('recorded_ogg', Text),
                   Column('recorded_spx', Text),
                   Column('wiki_name', Text),
                   Column('slides_link', Text),

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
