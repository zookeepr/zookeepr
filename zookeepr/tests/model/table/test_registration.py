import datetime
import md5

from zookeepr.tests.model.table import *

class TestRegistration(TableTest):
    """Test the ``registration`` table.

    This table stores registration and confirmation states.

    ``timestamp`` is the time stamp of the account creation.

    ``account_id`` references the account that contains the login
    details for this registration, which has not yet been activated.

    ``url_hash`` stores a hash used by the confirmation system to
    identify this registration.
    """
    table = 'core.tables.registration'
    samples = [dict(_timestamp=datetime.datetime.now(),
                    url_hash=md5.new("snuh").hexdigest(),
                    account_id=1,
                    ),
               dict(_timestamp=datetime.datetime(2006,05,30,14,31,37),
                    url_hash='winnebago',
                    account_id=1,
                    ),
               ]
    not_nullables=['_timestamp', 'url_hash', 'account_id']
