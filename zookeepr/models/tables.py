from sqlalchemy import *

person = Table('person',
               Column('id', Integer, primary_key=True),

               Column('account_id', Integer,
                      ForeignKey('account.id'),
                      ),
               
               # secondary key, unique identifier within the zookeepr app
               # useful for URLs
               Column('handle', String(40), unique=True, nullable=False),
               
               # login identifier and primary method of communicating

               # other personal details
               # the lengths of the fields are chosen arbitrarily
               Column('firstname', String(1024)),
               Column('lastname', String(1024)),
               Column('phone', String(32)),
               Column('fax', String(32)),
)

# types of submissions: typically 'paper', 'miniconf', etc
submission_type = Table('submission_type',
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40),
                               # FIXME workaround bug in sqlalchemy 0.1.7
                               unique='submission_type_name_unique',
                               nullable=False)
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

role = Table('role',
             Column('id', Integer, primary_key=True),

             # name of role
             Column('name', String,
                    # FIXME: workaround a bug in SQLAlchemy 0.1.7
                    unique='role_ux_name',
                    nullable=False)
             )

person_role_map = Table('person_role_map',
                        Column('person_id', Integer, ForeignKey('person.id')),
                        Column('role_id', Integer, ForeignKey('role.id'))
                        )

registration = Table('registration',
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

account = Table('account',
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
