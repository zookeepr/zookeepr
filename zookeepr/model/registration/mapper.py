from sqlalchemy import mapper, join, relation

from tables import registration
from zookeepr.model.core.tables import account, person
from domain import Registration
from zookeepr.model.core import Person

mapper(Registration, join(join(account, person), registration),
       properties = {
    'person': relation(Person)
    }
       )
