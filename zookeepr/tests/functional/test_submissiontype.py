from zookeepr.tests import *
from zookeepr.models import *

class TestSubmissiontypeController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='submissiontype'))
        # Test response...

    def test_new(self):
        res = self.app.get(url_for(controller='submissiontype', action='new'))

        res.mustcontain('Name:')

        res = self.app.get(url_for(controller='submissiontype', action='new'), params=dict(name='Paper'))

        # follow redirect
        res = res.follow()

        res.mustcontain('view subtype Paper')

        
