from sqlalchemy import mapper, join, relation

from zookeepr.model.core import Person
from tables import registration, accommodation_location, accommodation_option
from domain import Registration, Accommodation

mapper(Accommodation, join(accommodation_location, accommodation_option),
       properties = {
    'accommodation_location_id': [accommodation_location.c.id, accommodation_option.c.accommodation_location_id],
    'name': accommodation_location.c.name,
    'option': accommodation_option.c.name,
#    'available': outerjoin(join(accommodation_location, accommodation_option),
#                           registration,
#                           accommodation_option.c.id==registration.c.accommodation)
    }
       )

mapper(Registration, registration,
       properties = {
    'person': relation(Person),
    'accommodation': relation(Accommodation, backref='registrations'),
    }
       )
