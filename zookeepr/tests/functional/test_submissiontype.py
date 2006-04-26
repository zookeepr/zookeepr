from zookeepr.tests import *

class TestSubmissiontypeController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='submissiontype'))
        # Test response...

    def test_new(self):
        res = self.app.get(url_for(controller='submissiontype'))
        f = res.form[0]

        f['name'] = 'Paper'

        res = f.submit()
