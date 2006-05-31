from zookeepr.tests import *

class TestHomeController(TestController):
    def test_index(self):
        """Test FIXME: does nothing"""
        response = self.app.get(url_for(controller='/home'))
        # Test response...
