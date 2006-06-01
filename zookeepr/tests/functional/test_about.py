from zookeepr.tests.functional import *

class TestAboutController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='/about'))
        # Test response...
