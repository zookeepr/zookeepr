from sqlalchemy import *

from zookeepr.model import metadata

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

