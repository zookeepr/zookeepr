from sqlalchemy import join, mapper

from zookeepr.model.core.tables import account, person
from zookeepr.model.core.domain import Person

# Map the Person object onto both the account and person tables
mapper(Person, join(account, person),
    properties = {'account_id': [account.c.id, person.c.account_id]}
    )
