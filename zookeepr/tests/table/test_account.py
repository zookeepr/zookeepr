from zookeepr.tests.table import *
import new

class TestAccountTable(TableTestBase):
    table = 'account'
    sample = dict(name='testguy',
                  email_address='testguy@example.org',
                  password='test',
                  active=False)
    not_nullables = ['name', 'email_address', 'active']
