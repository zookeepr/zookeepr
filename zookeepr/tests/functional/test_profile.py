from zookeepr.tests.functional import *

class TestProfileController(ControllerTest):
    def test_profile_view(self):
        # set up
        p = model.Person(email_address='testguy@example.org',
                         handle='testguy',
                         firstname='Testguy',
                         lastname='McTest',
                         password='p4ssw0rd',
                         )
        p.activated = True
        self.dbsession.save(p)
        self.dbsession.flush()

        pid = p.id

        # try to log in
        resp = self.app.get(url_for(controller='person',
            action='signin'))
        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f['password'] = 'p4ssw0rd'
        resp = f.submit()

        resp = self.app.get('/profile/%d' % p.id)

        resp.mustcontain("McTest")

        # clean up
        self.dbsession.delete(self.dbsession.query(model.Person).get(pid))
        self.dbsession.flush()


class TestSignedInProfileController(SignedInCRUDControllerTest):
    def test_profile_list(self):
        resp = self.app.get('/profile')

        resp = resp.follow()

        resp.mustcontain("Testguy McTest")


