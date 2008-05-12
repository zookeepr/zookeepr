from zookeepr.tests import *

class TestStaticContentController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='static_content'))
        # Test response...
