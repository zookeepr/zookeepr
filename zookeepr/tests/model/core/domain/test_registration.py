import datetime
import md5

from zookeepr.model.core.domain import Account
from zookeepr.tests.model import *

class TestAccountModel(ModelTest):
    model = 'Account'
    samples = [dict(
                    email_address='testguy@example.org',
                    password='password',
                    activated=True,
                    fullname='testguy mctest',
                    ),
               dict(timestamp=datetime.datetime(2006, 6, 25, 10, 11, 37),
                    email_address='testgirl@example.org',
                    password='password1',
                    activated=False,
                    fullname='test3',
                    ),
               ]
    mangles = dict(password=lambda p: md5.new(p).hexdigest())

    def test_select_by_url_hash(self):
        self.check_empty_session()

        session = create_session()

        r = Account(email_address="testguy@example.org",
                         password="password")

        print r

        session.save(r)
        session.flush()

        s = session.query(Account).select_by(_url_hash=r.url_hash)

        # only one element
        self.assertEqual(1, len(s))
        # and it looks like r
        self.assertEqual(r, s[0])

        # clean up
        session.delete(r)
        session.flush()

        self.check_empty_session()
