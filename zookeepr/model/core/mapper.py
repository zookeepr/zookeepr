from sqlalchemy import mapper, join, relation, backref

from zookeepr.model.core.tables import account, person, role, person_role_map
from zookeepr.model.core.domain import Person, Role

# Map the Person object onto person table
mapper(Person, join(account, person),
       properties = {
    'account_id': [account.c.id, person.c.account_id],
    'roles': relation(Role, secondary=person_role_map, lazy=False,
                      backref='people')
    }
              )

# Map the Role object onto the role table
mapper(Role, role)
