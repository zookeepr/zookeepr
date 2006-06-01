from zookeepr.tests.functional import *

class TestAccountController(ControllerTest):
#     def test_index(self):
#         response = self.app.get(url_for(controller='person'))
#         # Test response...
#         response.mustcontain("person index")

    def test_signin(self):
        """Test account sign in"""
        # create a user
        p = model.Person(handle='testguy',
                         email_address='testguy@example.org',
                         password='p4ssw0rd')
        self.session.save(p)
        self.session.flush()
        
        # try to log in
        u = url_for(controller='/account', action='signin')
        params = {'username': 'testguy',
                  'password': 'p4ssw0rd',
                  'go': 'Submit'}
        res = self.app.post(u, params)
        self.failUnless(res.request.environ['REMOTE_USER'] == 'testguy')
        
        # clean up
        self.session.delete(p)
        self.session.flush()

    def test_signout(self):
        """Test account sign out"""

        # create a user
        p = model.Person(handle='testguy',
                         email_address='testguy@example.org',
                         password='p4ssw0rd')
        self.session.save(p)
        self.session.flush()

        # login
        u = url_for(controller='/account', action='signin')
        params = {'username': 'testguy',
                  'password': 'p4ssw0rd',
                  'go': 'Submit'}
        res = self.app.post(u, params)

        # logout
        u = url_for(controller='/account', action='signout')
        res = self.app.get(u)
        self.failIf(res.request.environ.has_key('REMOTE_USER'))

        # clean up
        self.session.delete(p)
        self.session.flush()


    def test_signin_invalid(self):
        """Test invalid login details"""
        # login
        u = url_for(controller='/account', action='signin')
        params = {'username': 'testguy',
                  'password': 'p4ssw0rd',
                  'go': 'Submit'}
        res = self.app.post(u, params)

        self.failIf(res.request.environ.has_key('REMOTE_USER'))
