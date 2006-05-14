from zookeepr.tests import *
from zookeepr.models import *

class TestSecurityController(TestController):
#     def test_index(self):
#         response = self.app.get(url_for(controller='person'))
#         # Test response...
#         response.mustcontain("person index")

    def test_signin(self):
        """Test account sign in"""
        # create a user
        p = Person(handle='testguy',
                   email_address='testguy@example.org',
                   password='p4ssw0rd')
        objectstore.flush()
        
        # try to log in
        u = url_for(controller='/security', action='signin')
        params = {'username': 'testguy',
                  'password': 'p4ssw0rd',
                  'go': 'Submit'}
        res = self.app.post(u, params)
        self.failUnless(res.request.environ['REMOTE_USER'] == 'testguy')
        # clean up
        p.delete()
        objectstore.flush()

    def test_signout(self):
        """Test account sign out"""

        # create a user
        p = Person(handle='testguy',
                   email_address='testguy@example.org',
                   password='p4ssw0rd')
        objectstore.flush()

        # login
        u = url_for(controller='/security', action='signin')
        params = {'username': 'testguy',
                  'password': 'p4ssw0rd',
                  'go': 'Submit'}
        res = self.app.post(u, params)

        # logout
        u = url_for(controller='/security', action='signout')
        res = self.app.get(u)
        self.failIf(res.request.environ.has_key('REMOTE_USER'))

        # clean up
        p.delete()
        objectstore.flush()

    def test_signin_invalid(self):
        """Test invalid login details"""
        # login
        u = url_for(controller='/security', action='signin')
        params = {'username': 'testguy',
                  'password': 'p4ssw0rd',
                  'go': 'Submit'}
        res = self.app.post(u, params)

        self.failIf(res.request.environ.has_key('REMOTE_USER'))
