from sqlalchemy import *

from zookeepr.model import metadata

accommodation_location = Table('accommodation_location', metadata, 
                               Column('id', Integer, primary_key=True),

                               Column('name', Text, nullable=False, unique=True),
                               Column('beds', Integer, nullable=False),
                               )

accommodation_option = Table('accommodation_option', metadata,
                             Column('id', Integer, primary_key=True),

                             Column('accommodation_location_id', Integer,
                                    ForeignKey('accommodation_location.id'),
                                    nullable=False),

                             Column('name', Text),
                             Column('cost_per_night', Float, nullable=False),
                             )

registration = Table('registration', metadata,
                     Column('id', Integer, primary_key=True),

                     Column('person_id', Integer, ForeignKey('person.id'),
                            unique=True),

                     Column('accommodation_option_id', Integer, ForeignKey('accommodation_option.id'),
                            ),
                     
                     Column('address1', Text),
                     Column('address2', Text),
                     Column('city', Text),
                     Column('state', Text),
                     Column('country', Text),
                     Column('postcode', Text),
                     Column('phone', Text),
                     Column('company', Text),
                     Column('nick', Text),
                     Column('shell', Text),
                     Column('shelltext', Text),
                     Column('editor', Text),
                     Column('editortext', Text),
                     Column('distro', Text),
                     Column('distrotext', Text),
                     Column('silly_description', Text),
                     Column('type', Text),
                     Column('voucher_code', Text),
                     Column('teesize', Text),
                     Column('extra_tee_count', Integer),
                     Column('extra_tee_sizes', Text),
                     Column('dinner', Integer),
                     Column('diet', Text),
                     Column('special', Text),
                     Column('volunteer', Text),
                     Column('opendaydrag', Integer),
                     Column('partner_email', Text),
                     Column('kids_0_3', Integer),
                     Column('kids_4_6', Integer),
                     Column('kids_7_9', Integer),
                     Column('kids_10_11', Integer),
                     Column('kids_12_17', Integer),
                     Column('pp_adults', Integer),
                     Column('speaker_pp_pay_adult', Integer),
                     Column('speaker_pp_pay_child', Integer),

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

                     Column('creation_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp()),
                     Column('last_modification_timestamp', DateTime,
                        nullable=False,
                        default=func.current_timestamp(),
                        onupdate=func.current_timestamp()),

                     )

rego_note = Table('rego_note', metadata,
    Column('id', Integer, primary_key=True),
    Column('rego_id', Integer, ForeignKey('registration.id')),
    Column('note', Text),
    Column('by_id', Integer, ForeignKey('person.id'), nullable=False),
    Column('entered', DateTime, default=func.current_timestamp()),
)
