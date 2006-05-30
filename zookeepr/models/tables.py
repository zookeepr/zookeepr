from sqlalchemy import *

metadata = DynamicMetaData(name="zookeepr core")

account = Table('account', metadata,
                Column('id', Integer, primary_key=True),

                Column('email_address', String,
                       nullable=False,
                       # FIXME: when sqla 0.2 comes out, change this to True
                       unique='account_email_address_ux'),
                
                Column('password_hash', String),

                # flag that the account has been activated by the user
                # (responded to their confirmation email)
                Column('activated', Boolean,
                       PassiveDefault("false"),
                       nullable=False),
                )

person = Table('person', metadata,
               Column('id', Integer, primary_key=True),

               Column('account_id', Integer,
                      ForeignKey('account.id'),
                      ),
               
               # secondary key, unique identifier within the zookeepr app
               # useful for URLs, not required though (a-la flickr)
               Column('handle', String(40),
                      # FIXME: replace when using SA 0.2
                      unique='ux_person_handle',
                      ),
               
               # other personal details
               # the lengths of the fields are chosen arbitrarily
               Column('firstname', String(1024)),
               Column('lastname', String(1024)),
               Column('phone', String(32)),
               Column('fax', String(32)),
)

# types of submissions: typically 'paper', 'miniconf', etc
submission_type = Table('submission_type', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40),
                               unique=True,
                               nullable=False),
                        )

# submissions to the conference
submission = Table('submission', metadata,
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

# describe account roles to grant levels of access
role = Table('role', metadata,
              Column('id', Integer, primary_key=True),

              # name of role
              Column('name', String,
                     # FIXME: workaround a bug in SQLAlchemy 0.1.7
                     unique='role_ux_name',
                     nullable=False)
              )

person_role_map = Table('person_role_map', metadata,
                        Column('person_id', Integer, ForeignKey('person.id')),
                        Column('role_id', Integer, ForeignKey('role.id'))
                        )

registration = Table('registration', metadata,
                     Column('id', Integer, primary_key=True),
                     
                     # timestamp of the registration for expiration
                     # FIXME: expiration of rows not currently implemented
                     Column('timestamp', DateTime,
                            nullable=False,
                            ),

                     # link to the account details
                     Column('person_id', Integer,
                            ForeignKey('person.id'),
                            ),

                     # hash of the url generated for easy lookup
                     Column('url_hash', String(32),
                            nullable=False,
                            index=True,
                            ),
                     )
