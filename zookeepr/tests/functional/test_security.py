from zookeepr.tests import *
from zookeepr.models import *

class TestSecurityController(TestController):
#     def test_index(self):
#         response = self.app.get(url_for(controller='person'))
#         # Test response...
#         response.mustcontain("person index")

    def test_signin(self):
        """Test account sign in"""
        u = url_for(controller='/security', action='signin')
        params = {'username': 'testguy',
                  'password': 'testguy',
                  'go': 'Submit'}
        res = self.app.post(u, params)
        self.failUnless(res.request.environ['REMOTE_USER'] == 'testguy')

    def test_signout(self):
        """Test account sign out"""
        u = url_for(controller='/security', action='signin')
        params = {'username': 'testguy',
                  'password': 'testguy',
                  'go': 'Submit'}
        res = self.app.post(u, params)
        
        u = url_for(controller='/security', action='signout')
        res = self.app.get(u)
        #print res.request.environ
        #res.showbrowser()
        self.failIf(res.request.environ.has_key('REMOTE_USER'))
