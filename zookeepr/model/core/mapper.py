from sqlalchemy import join, mapper

from zookeepr.model.core.tables import person
from zookeepr.model.core.domain import Person

# Map the Person object onto person table
mapper(Person, person)
