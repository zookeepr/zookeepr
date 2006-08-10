import sqlalchemy.mods.threadlocal
from sqlalchemy import assign_mapper

from zookeepr.model.core.tables import person
from zookeepr.model.core.domain import Person

# Map the Person object onto person table
assign_mapper(Person, person)
