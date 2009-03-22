from sqlalchemy import *

from zookeepr.model import metadata

                
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

