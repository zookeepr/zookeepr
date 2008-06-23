from sqlalchemy import *

from zookeepr.model import metadata

db_content_type = Table('db_content_type', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40),
                               unique=True,
                               nullable=False),
                        )

db_content = Table('db_content', metadata,
                     Column('id', Integer, primary_key=True),

                     Column('title', Text),
                     Column('type_id', Integer, ForeignKey('db_content_type.id')),
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
