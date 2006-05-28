from zookeepr.tests.table import *

class TestAccountTable(TableTestBase):
    """Test the ``account`` table.

    This table stores the basic login information for a user,
    and is used with the registration confirmation system to ensure that
    accounts are correctly activated before use.

    Personal details associated with this account (i.e. handle, full name,
    address, phone numner, etc) are kept in the ``person`` table, which is
    linked here via a foreign key.

    Users log in with only their ``email_address`` and a ``password``, which
    is stored hashed in this table (but we don't care how here).
    """
    table = 'account'
    sample = [dict(email_address='testguy@example.org',
                   password='test',
                   activated=False),
              dict(email_address='testgirl@examplr.com',
                   password='p4ssw0rd',
                   activated=True)]
    not_nullables = ['email_address', 'activated']
    uniques = ['email_address']
    
