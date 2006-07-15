import datetime
import md5

from zookeepr.models import Registration
from zookeepr.tests.model import *

class TestRegistrationModel(ModelTest):
    model = 'Registration'
    samples = [dict(
                    email_address='testguy@example.org',
                    password='password',
                    activated=True,
                    ),
               dict(timestamp=datetime.datetime(2006, 6, 25, 10, 11, 37),
                    email_address='testgirl@example.org',
                    password='password1',
                    activated=False,
                    ),
               ]
    mangles = dict(password=lambda p: md5.new(p).hexdigest())

    def test_select_by_url_hash(self):
        self.check_empty_session()

        session = create_session()

        r = Registration(email_address="testguy@example.org",
                         password="password")

        print r

        session.save(r)
        session.flush()

        s = session.query(Registration).select_by_url_hash(r.url_hash)

        self.assertEqual(r, s)
