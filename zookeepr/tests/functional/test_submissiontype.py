from zookeepr.tests import *

class TestSubmissiontypeController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='submissiontype'))
        # Test response...
