from sqlalchemy import *

from zookeepr.model import metadata

registration_product = Table('registration_product', metadata,
                             Column('registration_id', Integer, ForeignKey('registration.id'), primary_key=True),
                             Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
                             Column('qty', Integer, nullable=False),
                            )

registration = Table('registration', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('person_id', Integer, ForeignKey('person.id'), unique=True),
                     Column('over18', Boolean),
                     Column('nick', Text),
                     Column('shell', Text),
                     Column('editor', Text),
                     Column('distro', Text),
                     Column('silly_description', Text),
                     Column('keyid', Text),
                     Column('planetfeed', Text),
                     Column('voucher_code', Text, unique=True),
                     Column('diet', Text),
                     Column('special', Text),
                     Column('volunteer', Text),
                     Column('opendaydrag', Integer),
                     Column('partner_email', Text),
                     Column('checkin', Integer),
                     Column('checkout', Integer),
                     Column('lasignup', Boolean),
                     Column('announcesignup', Boolean),
                     Column('delegatesignup', Boolean),
                     Column('speaker_record', Boolean),
                     Column('speaker_video_release', Boolean),
                     Column('speaker_slides_release', Boolean),
                     Column('prevlca', PickleType),
                     Column('miniconf', PickleType),
                     Column('creation_timestamp', DateTime, nullable=False, default=func.current_timestamp()),
                     Column('last_modification_timestamp', DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp()),
                    )

rego_note = Table('rego_note', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('rego_id', Integer, ForeignKey('registration.id')),
                  Column('note', Text),
                  Column('by_id', Integer, ForeignKey('person.id'), nullable=False),
                  Column('entered', DateTime, default=func.current_timestamp()),
                 )
