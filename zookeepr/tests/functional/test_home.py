from zookeepr.tests.functional import *

class TestHomeController(ControllerTest):
    def test_index(self):
        response = self.app.get(url_for(controller='home'))
