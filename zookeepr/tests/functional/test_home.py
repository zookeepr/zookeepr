from zookeepr.model import Person, Submission
from zookeepr.tests.functional import *

class TestHomeController(ControllerTest):
    def test_index(self):
        response = self.app.get(url_for(controller='home'))

    def test_index_logged_in(self):
        p = Person(email_address='testguy@example.org',
                   password='test',
                   firstname='Testguy')
        p.activated = True
        p.save()
        print p
        s = Submission(title='foo')
        s.save()
        p.submissions.append(s)
        p.flush()
        s.flush()

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
        
        p.delete()
        s.delete()
        p.flush()
        s.flush()
