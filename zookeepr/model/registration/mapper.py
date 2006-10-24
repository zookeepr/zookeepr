from sqlalchemy import mapper, join

from tables import registration
from zookeepr.model.core.tables import account, person
from domain import Registration

mapper(Registration, join(join(account, person), registration),
       properties = {
    'account_id': [account.c.id, person.c.account_id, registration.c.account_id],
    }
       )
