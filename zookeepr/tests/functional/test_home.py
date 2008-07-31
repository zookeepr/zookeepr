from zookeepr.tests.functional import *

class TestHomeController(ControllerTest):
    def test_index(self):
        response = self.app.get(url_for(controller='home'))

    def test_index_logged_in(self):
        p = model.Person(email_address='testguy@example.org',
                   password='test',
                   firstname='Testguy',
                   lastname='Testguy',
		   handle='testguy')
        p.activated = True
        self.dbsession.save(p)
        print p
        s = model.Proposal(title='foo')
        self.dbsession.save(s)
        p.proposals.append(s)

        self.dbsession.flush()

        print p

        pid = p.id
        sid = s.id

        resp = self.app.get(url_for(controller='person',action='signin'))
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
        resp.mustcontain("Sign out")

        self.dbsession.delete(self.dbsession.query(model.Proposal).get(sid))
        self.dbsession.delete(self.dbsession.query(model.Person).get(pid))
        self.dbsession.flush()
