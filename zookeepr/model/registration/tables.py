import sqlalchemy.mods.threadlocal
from sqlalchemy import *

registration = Table('registration',
                     Column('id', Integer, primary_key=True),

                     Column('person_id', Integer, ForeignKey('person.id')),

                     Column('address1', String),
                     Column('address2', String),
                     Column('city', String),
                     Column('state', String),
                     Column('country', String),
                     Column('postcode', String),
                     Column('phone', String),
                     Column('company', String),
                     Column('shell', String),
                     Column('shelltext', String),
                     Column('editor', String),
                     Column('editortext', String),
                     Column('distro', String),
                     Column('distrotext', String),
                     Column('silly_description', String),
                     Column('type', String),
                     Column('discount_code', String),
                     Column('teesize', String),
                     Column('dinner', Integer),
                     Column('diet', String),
                     Column('special', String),
                     Column('opendaydrag', Integer),
                     Column('partner_email', String),
                     Column('kids_0_3', Integer),
                     Column('kids_4_6', Integer),
                     Column('kids_7_9', Integer),
                     Column('kids_10', Integer),
                     Column('accommodation', String),
                     Column('checkin', Integer),
                     Column('checkout', Integer),
                     Column('lasignup', Boolean),
                     Column('announcesignup', Boolean),
                     Column('delegatesignup', Boolean),
                     Column('prevlca', PickleType),
                     Column('miniconf', PickleType),

                     Column('creation_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp()),
                     Column('last_modification_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp(),
                        onupdate=func.current_timestamp()),

                     )

accommodation = Table('accommodation',
                      Column('id', Integer, primary_key=True),

                      Column('name', String),
                      Column('cost_per_night', Float),
                      Column('beds', Integer),
                      )

accommodation_option = Table('accommodation_option',
                             Column('id', Integer, primary_key=True),

                             Column('name', String, nullable=False, unique=True),
                             Column('cost_per_night', Float, nullable=False),
                             )
accommodation_location = Table('accommodation_location',
                               Column('id', Integer, primary_key=True),

                               Column('name', String, nullable=False, unique=True),
                               Column('beds', Integer, nullable=False),
                               )
