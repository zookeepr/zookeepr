from sqlalchemy import *

from zookeepr.model import metadata

print func, dir(func)
print func.current_timestamp, dir(func.current_timestamp)

invoice = Table('invoice', metadata,
                Column('id', Integer, primary_key=True),

                Column('person_id', Integer,
                       ForeignKey('person.id'),
                       nullable=False,
                       ),

                Column('issue_date', Date,
                       default=func.current_date(),
                       nullable=False),
                
                Column('creation_timestamp', DateTime,
                       nullable=False,
                       default=func.current_timestamp()),
                Column('last_modification_timestamp', DateTime,
                       nullable=False,
                       default=func.current_timestamp(),
                       onupdate=func.current_timestamp()),

                )

invoice_item = Table('invoice_item', metadata,
                     Column('id', Integer, primary_key=True),

                     Column('invoice_id', Integer,
                            ForeignKey('invoice.id'),
                            nullable=False),
                     
                     Column('description', String,
                            nullable=False),
                     Column('cost', Float,
                            nullable=False),
                     )

# for doing n-n mappings of invoice and registrations
invoice_registration_map = Table('invoice_registration_map', metadata,
    Column('invoice_id', Integer, ForeignKey('invoice.id'),
           unique=True,
        nullable=False),
    Column('registration_id', Integer, ForeignKey('registration.id'),
           unique=True,
        nullable=False),
    )

