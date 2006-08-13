from sqlalchemy import mapper, relation, backref

from zookeepr.model.core.tables import person, role, person_role_map
from zookeepr.model.core.domain import Person, Role

# Map the Person object onto person table
mapper(Person, person,
       properties = {
    'roles': relation(Role, secondary=person_role_map, lazy=False,
                      backref='people')
    }
              )

# Map the Role object onto the role table
mapper(Role, role)
