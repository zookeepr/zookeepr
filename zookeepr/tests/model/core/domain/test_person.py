import datetime
import md5

from zookeepr.tests.model import *

class TestPerson(CRUDModelTest):
    domain = model.core.Person

    samples = [dict(handle='testguy',
                    email_address='testguy@example.org',
                    password='p4ssw0rd',
                    fullname='Testguy McTest',
                    phone='+61295555555',
                    activated=True,
                    creation_timestamp=datetime.datetime(2006,6,25,10,11,37),
                    ),
               dict(handle='testgirl',
                    email_address='testgrrl@example.com',
                    password='foobar',
                    fullname='Testgirl Van test',
                    phone="37",
                    fax="42",
                    activated=False,
                    ),
               ]

    mangles = dict(password=lambda p: md5.new(p).hexdigest())

    def test_select_by_url(self):
        self.check_empty_session()

        r = model.Person(email_address='testguy@testguy.org',
                   password='password')

        print r

        self.dbsession.save(r)
        self.dbsession.flush()

        s = self.dbsession.query(model.Person).select_by(url_hash=r.url_hash)

        # only one element
        self.assertEqual(1, len(s))

        # and it looks like r
        self.assertEqual(r, s[0])

        # clean up
        self.dbsession.delete(r)
        self.dbsession.flush()

        self.check_empty_session()
