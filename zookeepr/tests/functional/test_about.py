from zookeepr.tests.functional import *

class TestAboutController(ControllerTest):
    def test_index(self):
        response = self.app.get(url_for(controller='/about'))
        # Test response...

    def test_view_contact(self):
        response = self.app.get(url_for(controller='about',
                                        action='view',
                                        id='contact'))
