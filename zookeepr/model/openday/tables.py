from sqlalchemy import *

from zookeepr.model import metadata

openday = Table('openday', metadata,
                     Column('id', Integer, primary_key=True),

                     Column('firstname', Text),
                     Column('lastname', Text),
                     Column('email_address', Text),
                     Column('heardfrom', Text),
                     Column('heardfromtext', Text),
                     Column('opendaydrag', Integer),

                     Column('creation_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp()),
                     Column('last_modification_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp(),
                        onupdate=func.current_timestamp()),

                     )
