from zookeepr.tests.functional import *

class TestSubmission(ControllerTest):
    model = model.Submission
    name = 'submission'
    url = '/submission'
    samples = [dict(title='test',
                    abstract='abstract 1',
                    experience='experience 1',
                    url='',
                    submission_type=1,
                    ),
               dict(title='not a test',
                    abstract='abstract 2',
                    experience='experience 2',
                    submission_type=1,
                    url='',
                    ),
               ]

    def setUp(self):
        ControllerTest.setUp(self)
        model.submission_type.insert().execute(
            dict(id=1, name='Paper'),
            )
        model.submission_type.insert().execute(
            dict(id=2, name='Presentation'),
            )
        model.submission_type.insert().execute(
            dict(id=3, name='Miniconf'),
            )

    def tearDown(self):
        model.submission_type.delete().execute()
        ControllerTest.tearDown(self)
