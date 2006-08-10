from zookeepr.tests.functional import *

class TestSubmissionType(ControllerTest):
    model = model.submission.domain.SubmissionType
    name = 'submissiontype'
    url = '/submissiontype'
    samples = [dict(name='Paper'),
               dict(name='BOF')]
