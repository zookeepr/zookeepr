from zookeepr.model import Person, Proposal
from zookeepr.tests.functional import *

class TestHomeController(ControllerTest):
    def test_index(self):
        response = self.app.get(url_for(controller='home'))

    def test_index_logged_in(self):
        p = Person(email_address='testguy@example.org',
                   password='test',
                   firstname='Testguy')
        p.activated = True
        self.objectstore.save(p)
        print p
        s = Proposal(title='foo')
        self.objectstore.save(s)
        p.proposals.append(s)

        self.objectstore.flush()

        print p

        resp = self.app.get(url_for(controller='account',action='signin'))
        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f['password'] = 'test'
        resp = f.submit()
        print resp
        print resp.session
        self.failUnless('person_id' in resp.session)
        self.assertEqual(p.id,
                         resp.session['person_id'])
        resp = resp.follow()
        print resp.request.url
        self.assertEqual('/', resp.request.url)
        resp.mustcontain("Welcome, <strong>Testguy</strong>!")
        resp.mustcontain("foo")

        self.objectstore.delete(p)
        self.objectstore.delete(s)
        self.objectstore.flush()
