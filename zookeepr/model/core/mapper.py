from sqlalchemy import join, mapper

from zookeepr.model.core.tables import account, person, registration
from zookeepr.model.core.domain import Person, Account

# Map the Person object onto both the account and person tables
mapper(Person, join(account, person),
    properties = {
        'account_id': [account.c.id, person.c.account_id],
    }
    )

# map account on to account and registration
mapper(Account, join(account, registration),
    properties = {
        'account_id': [account.c.id, registration.c.account_id],
    }
    )
