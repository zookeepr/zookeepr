from sqlalchemy import mapper, join, relation

from zookeepr.model.core import Person
from tables import registration, accommodation_location, accommodation_option
from domain import Registration, Accommodation

mapper(Registration, registration,
       properties = {
    'person': relation(Person)
    }
       )

mapper(Accommodation, join(accommodation_location, accommodation_option),
       properties = {
    'name': accommodation_location.c.name,
    'option': accommodation_option.c.name,
    }
       )
