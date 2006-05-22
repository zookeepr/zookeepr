from zookeepr.tests import *

class TestInfoController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='/info'))
        # Test response...