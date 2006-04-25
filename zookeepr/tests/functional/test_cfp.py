from zookeepr.tests import *

class TestCfpController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='/cfp'))
        # Test response...
        response.mustcontain("perhaps you'd like to")

    def test_new(self):
        """Test that one can create a new submission"""
        res = self.app.get(url_for(controller='/cfp', action='new'))

        res.mustcontain("you're creating a new submission")
        res.mustcontain("powered by zookeepr")
