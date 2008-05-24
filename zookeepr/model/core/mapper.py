from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy.sql import join

from tables import person, role, person_role_map, password_reset_confirmation
from domain import Person, Role, PasswordResetConfirmation
from zookeepr.model.billing.domain import Invoice

# Map the Person object onto person table
mapper(Person, person,
       properties = {
    'roles': relation(Role, secondary=person_role_map, lazy=False,
                      backref='people'),
    'invoice': relation(Invoice)
    }
              )

# Map the Role object onto the role table
mapper(Role, role)

# Map the PasswordResetConfuirmation object
mapper(PasswordResetConfirmation, password_reset_confirmation)
