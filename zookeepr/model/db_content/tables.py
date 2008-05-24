from sqlalchemy import *

from zookeepr.model import metadata

db_content = Table('db_content', metadata,
                     Column('id', Integer, primary_key=True),

                     Column('title', Text),
                     Column('url', Text),
                     Column('body', Text),

                     Column('creation_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp()),
                     Column('last_modification_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp(),
                        onupdate=func.current_timestamp()),
                     )
