from sqlalchemy import *

from zookeepr.model import metadata

person = Table('person', metadata,
                Column('id', Integer, primary_key=True),

                Column('email_address', String,
                       nullable=False,
                       unique=True),

                Column('password_hash', String),


                # creation timestamp of the registration
                Column('creation_timestamp', DateTime,
                       nullable=False,
                       ),

                # hash of the url generated for easy lookup
                Column('url_hash', String(32),
                       nullable=False,
                       index=True,
                       ),

                # flag that the account has been activated by the user
                # (responded to their confirmation email)
                Column('activated', Boolean,
                       nullable=False),

               # other personal details
               # the lengths of the fields are chosen arbitrarily
               Column('firstname', String(1024)),
               Column('lastname', String(1024)),
               Column('phone', String(32)),
               Column('mobile', String(32)),

               Column('url', String()),

               # Proposal bits
               Column('experience', String()),
               Column('bio', String()),
              )

# describe account roles to grant levels of access
role = Table('role', metadata,
             Column('id', Integer, primary_key=True),

             # name of role
             Column('name', String,
                    unique=True,
                    nullable=False),
             )

# map persons onto roles
person_role_map = Table('person_role_map', metadata,
                        Column('person_id', Integer, ForeignKey('person.id')),
                        Column('role_id', Integer, ForeignKey('role.id'))
                        )

# password reset confirmation
password_reset_confirmation = Table('password_reset_confirmation', metadata,
    Column('id', Integer, primary_key=True),

    Column('email_address', String,
        nullable=False,
        unique=True,
        ),
    Column('url_hash', String,
        nullable=False,
        unique=True,
        ),
    Column('timestamp', DateTime,
        nullable=False,
        ),
    )

