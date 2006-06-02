from zookeepr.tests.functional import *

class TestAboutController(ControllerTest):
    def test_index(self):
        response = self.app.get(url_for(controller='/about'))
        # Test response...
