from sqlalchemy import mapper, join, relation

from zookeepr.model.core import Person
from tables import registration, accommodation
from domain import Registration, Accommodation

mapper(Registration, registration,
       properties = {
    'person': relation(Person)
    }
       )

mapper(Accommodation, accommodation)
