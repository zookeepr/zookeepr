from zookeepr.tests import *

class TestPeopleController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='/people'))
        # Test response...
        response.mustcontain("people index")
