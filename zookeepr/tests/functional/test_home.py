from zookeepr.tests.functional import *

class TestHomeController(ControllerTest):
    def test_index(self):
        response = self.app.get(url_for(controller='home'))

    def test_index_logged_in(self):
        p = model.Person(email_address='testguy@example.org',
                   password='test',
                   firstname='Testguy')
        p.activated = True
        objectstore.save(p)
        print p
        s = model.Proposal(title='foo')
        objectstore.save(s)
        p.proposals.append(s)

        objectstore.flush()

        print p

        pid = p.id
        sid = s.id

        resp = self.app.get(url_for(controller='account',action='signin'))
        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f['password'] = 'test'
        resp = f.submit()
        print resp
        print resp.session
        self.failUnless('signed_in_person_id' in resp.session)
        self.assertEqual(p.id,
                         resp.session['signed_in_person_id'])
        resp = resp.follow()
        print resp.request.url
        self.assertEqual('/', resp.request.url)
        resp.mustcontain("signed in")
        resp.mustcontain("foo")

        objectstore.delete(Query(model.Proposal).get(sid))
        objectstore.delete(Query(model.Person).get(pid))
        objectstore.flush()
