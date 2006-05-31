from zookeepr.tests.functional import *

class TestSubmission(ControllerTest):
    model = model.Submission
    name = 'submission'
    url = '/submission'
    samples = [dict(title='test'),
               dict(title='not a test'),
               ]
