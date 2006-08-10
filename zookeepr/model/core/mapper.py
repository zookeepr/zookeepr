import sqlalchemy.mods.threadlocal
from sqlalchemy import assign_mapper, relation, backref

from zookeepr.model.core.tables import person, role, person_role_map
from zookeepr.model.core.domain import Person, Role

# Map the Person object onto person table
assign_mapper(Person, person)

# Map the Role object onto the role table
assign_mapper(Role, role,
              properties = {
    'people': relation(Person, secondary=person_role_map,
                       backref=backref('roles', lazy=True))
    }
              )
