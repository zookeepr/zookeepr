from sqlalchemy import *

openday = Table('openday',
                     Column('id', Integer, primary_key=True),

                     Column('fullname', String),
                     Column('email_address', String),
                     Column('heardfrom', String),
                     Column('heardfromtext', String),
                     Column('opendaydrag', Integer),

                     Column('creation_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp()),
                     Column('last_modification_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp(),
                        onupdate=func.current_timestamp()),

                     )
