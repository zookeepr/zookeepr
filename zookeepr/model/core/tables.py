from sqlalchemy import *

# FIXME - EVIL HACK
# For some unknown reason _engine disappears
# So we save it in evil_jf and and restore it each request in __before__
evil_jf = {}


account = Table('account',
                Column('id', Integer, primary_key=True),

                Column('email_address', String,
                       nullable=False,
                       unique=True),
                
                Column('password_hash', String),

                # flag that the account has been activated by the user
                # (responded to their confirmation email)
                Column('activated', Boolean,
                       default=False,
                       nullable=False),
                )

person = Table('person',
               Column('id', Integer, primary_key=True),

               Column('account_id', Integer,
                      ForeignKey('account.id'),
                      ),
               
               # secondary key, unique identifier within the zookeepr app
               # useful for URLs, not required though (a-la flickr)
               Column('handle', String(40),
                      unique=True,
                      ),
               
               # other personal details
               # the lengths of the fields are chosen arbitrarily
               Column('firstname', String(1024)),
               Column('lastname', String(1024)),
               Column('phone', String(32)),
               Column('fax', String(32)),
)

# describe account roles to grant levels of access
role = Table('role',
              Column('id', Integer, primary_key=True),

              # name of role
              Column('name', String,
                     unique=True,
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
                            key='_timestamp',
                            ),

                     # link to the account details
                     Column('account_id', Integer,
                            ForeignKey('account.id'),
                            nullable=False,
                            ),

                     # hash of the url generated for easy lookup
                     Column('url_hash', String(32),
                            nullable=False,
                            index=True,
                            ),
                     )

__all__ = ['account', 'person', 'submission_type', 'submission', 'registration', 'person_role_map', 'role']
