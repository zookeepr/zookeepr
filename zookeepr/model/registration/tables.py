from sqlalchemy import *

from zookeepr.model import metadata
from zookeepr.lib.model import CommaList

rego_note = Table('rego_note', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('rego_id', Integer, ForeignKey('registration.id')),
                  Column('note', Text),
                  Column('by_id', Integer, ForeignKey('person.id'), nullable=False),
                  Column('creation_timestamp', DateTime, nullable=False, default=func.current_timestamp()),
                  Column('last_modification_timestamp', DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp()),
                 )
