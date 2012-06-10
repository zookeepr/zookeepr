import datetime
import md5

from zkpylons.tests.model import *

class TestPersonTable(TableTest):
    """Test the `person` table.

    This table stores the basic login information for a user, as well as data
    that handles the user's registration process.

    Auxiliary details about a person are stored in the `person` table, which is
    linked here by a 1-1 foreign key mapping.

    Users log in with only their ``email_address`` and ``password_hash``, which
    is typically stored hashed in this table (but we don't care how; we use MD5
    in upper layers of the business logic; here it's just a string).

    ``creation_timestamp`` is the time stamp of the person creation.

    ``url_hash`` stores a hash used by the confirmatoin sustem to identify this
    registration, typically made up of a hash of the email address, timestamp,
    and a nonce, but we don't deal with that at this layer.

    ``activated`` is a flag that indicates that the email address has been
    confirmed, and the user may log in.
    """
    # What's the table object?
    table = model.core.tables.person
    # What's some sample data we can use for the generic table testing?
    samples = [dict(email_address='testguy@example.org',
                    password_hash='password_hash1',
                    creation_timestamp=datetime.datetime(2006,8,14,9,2,37),
                    url_hash='url_hash1',
                    activated=True,
                    ),
               dict(email_address='testgirl@example.com',
                    password_hash='password-hash2',
                    creation_timestamp=datetime.datetime(2006,5,30,14,31,37),
                    url_hash='url_hash-2',
                    activated=False,
                    ),
               ]
    # These fields must not be null
    not_nullables = ['email_address', 'creation_timestamp', 'url_hash', 'activated']
    # These fields must have a unique index
    uniques = ['email_address']
