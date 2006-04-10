from zookeepr.tests import *

class TestSubmissionController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='/submission'))
        # Test response...