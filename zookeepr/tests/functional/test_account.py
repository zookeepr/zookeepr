from zookeepr.tests.functional import *

class TestAccountController(ControllerTest):
    
#     def test_account_signin_routing(self):
#         self.assertEqual(dict(controller='account',
#                               action='signin'),
#                          self.map.match('/account/signin'))

#     def test_account_signin_url(self):
#         self.assertEqual('/account/signin',
#                          url_for(controller='account', action='signin'))

#     def test_account_signout_url(self):
#         self.assertEqual('/account/signout',
#                          url_for(controller='account', action='signout'))

    def test_signin_signout(self):
        """Test account sign in"""
        # create a user
        p = model.Person(email_address='testguy@example.org',
                         password='p4ssw0rd')
        self.session.save(p)
        self.session.flush()
        
        # try to log in
        resp = self.app.get(url_for(controller='account',
                                    action='signin'))
        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f['password'] = 'p4ssw0rd'
        resp = f.submit()

        self.failUnless('person_id' in resp.session)
        self.assertEqual(p.id,
                         resp.session['person_id'])

        # sign out
        resp = resp.goto(url_for(controller='account',
                                 action='signout'))

        print "resp.session", resp.session

        self.failIf('contact_id' in resp.session)
        
        # clean up
        self.session.delete(p)
        self.session.flush()

    def test_signin_invalid(self):
        """Test invalid login details"""
        # login
        resp = self.app.get(url_for(controller='/account', action='signin'))
        f = resp.form
        f['email_address'] = 'testguy'
        f['password'] = 'password'

        f.submit()

        self.failIf('contact_id' in resp.session)
