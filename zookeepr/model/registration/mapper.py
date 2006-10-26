from sqlalchemy import mapper, join, relation

from zookeepr.model.core import Person
from tables import registration
from domain import Registration

mapper(Registration, registration,
       properties = {
    'person': relation(Person)
    }
       )
