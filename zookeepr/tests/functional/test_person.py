from zookeepr.tests import *

class TestPersonController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='/person'))
        # Test response...
        response.mustcontain("person index")
