from sqlalchemy import *

from zookeepr.model import metadata

person = Table('person', metadata,
                Column('id', Integer, primary_key=True),

                Column('email_address', Text,
                       nullable=False,
                       unique=True),

                Column('password_hash', Text),


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
               Column('firstname', Text),
               Column('lastname', Text),
               Column('address1', Text),
               Column('address2', Text),
               Column('city', Text),
               Column('state', Text),
               Column('postcode', Text),
               Column('country', Text),
               Column('company', Text),
               Column('phone', Text),
               Column('mobile', Text),

               Column('url', Text),

               # Proposal bits
               Column('experience', Text),
               Column('bio', Text),
              )

# describe account roles to grant levels of access
role = Table('role', metadata,
             Column('id', Integer, primary_key=True),

             # name of role
             Column('name', Text,
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

    Column('email_address', Text,
        nullable=False,
        unique=True,
        ),
    Column('url_hash', Text,
        nullable=False,
        unique=True,
        ),
    Column('timestamp', DateTime,
        nullable=False,
        ),
    )

