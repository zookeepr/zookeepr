import datetime
import md5

from zookeepr.tests.model import *

class TestPasswordResetConfirmationTable(TableTest):
    """Test the password_reset_confirmation table.

    This table stores active forgotten password reset processes.  When a
    user indicates that they want to change their password, they first get
    emailed a unique URL that they need to visit to copmlete the password
    change.  In order to do so, we keep a record in this table of the
    URL, the email address that the password change is for, and the time
    of the request (we expire password changes after 24 hours).
    """
    table = model.core.tables.password_reset_confirmation
    samples = [dict(email_address='testguy@example.org',
        url_hash='url_hash1',
        timestamp=datetime.datetime(2006,8,19,9,47,37),
        ),
        dict(email_address='testgirl@example.org',
        url_hash='url_hash2',
        timestamp=datetime.datetime.now(),
        ),
        ]
    # no fields can be null
    not_nullables = ['email_address', 'url_hash', 'timestamp']
    # must be unique
    uniques = ['url_hash', 'email_address']
