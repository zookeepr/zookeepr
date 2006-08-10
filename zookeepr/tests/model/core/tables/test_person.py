from zookeepr.tests.model import *

class TestPerson(TableTest):
    """Test the ``person`` table.

    This table stores the basic login information for a user,
    and is used with the registration confirmation system to ensure that
    accounts are correctly activated before use.

    This table also stores auxiliary information about a person: their name,
    their contact details, etc, and references an account table that
    contains the person's login details.

    Users log in with only their ``email_address`` and a ``password``, which
    is stored hashed in this table (but we don't care how here).
    
    This table stores registration and confirmation states.

    ``timestamp`` is the time stamp of the account creation.

    ``account_id`` references the account that contains the login
    details for this registration, which has not yet been activated.

    ``url_hash`` stores a hash used by the confirmation system to
    identify this registration.
    """
    table = 'core.tables.person'
    samples = [dict(handle='testguy',
                    account_id=1,
                    firstname='Testguy',
                    lastname='McTest',
                    phone='+61295555555',
                    fax='+61295555556',
                    email_address='testguy@example.org',
                    password_hash='test',
                    activated=False,
                    _creation_timestamp=datetime.datetime.now(),
                    url_hash=md5.new("snuh").hexdigest(),
                    account_id=1,
                    ),
               dict(handle='testgirl',
                    account_id=2,
                    firstname='Testgirl',
                    lastname='Van Test',
                    phone='+37',
                    fax='42',
                    email_address='testgirl@example.com',
                    password_hash='p4ssw0rd',
                    activated=True,
                    _creation_timestamp=datetime.datetime(2006,05,30,14,31,37),
                    url_hash='winnebago',
                    account_id=1,
                    ),
               ]
    not_nullables = ['email_address', '_creation_timestamp', 'url_hash', 'account_id']
    # FIXME: activated should be not nullable but also carries a default
    uniques = ['email_address', 'handle'
