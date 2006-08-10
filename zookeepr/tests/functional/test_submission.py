import pprint

from zookeepr.model import Submission, SubmissionType
from zookeepr.tests.functional import *

class TestSubmission(ControllerTest):
    name = 'submission'
    url = '/submission'
    samples = [dict(title='test',
                    abstract='abstract 1',
                    experience='experience 1',
                    url='http://example.org',
                    type=1,
                    ),
               dict(title='not a test',
                    abstract='abstract 2',
                    experience='experience 2',
                    type=2,
                    url='http://lca2007.linux.org.au',
                    ),
               ]

    def setUp(self):
        ControllerTest.setUp(self)
        model.submission.tables.submission_type.insert().execute(
            dict(id=1, name='Paper'),
            )
        model.submission.tables.submission_type.insert().execute(
            dict(id=2, name='Presentation'),
            )
        model.submission.tables.submission_type.insert().execute(
            dict(id=3, name='Miniconf'),
            )

    def tearDown(self):
        model.submission.tables.submission_type.delete().execute()
        ControllerTest.tearDown(self)

    def test_selected_radio_button_in_edit(self):
        # Test that a radio button is checked when editing a submission
        s = Submission(id=1,
                       type=SubmissionType.get(3),
                       title='foo',
                       abstract='bar',
                       experience='',
                       url='')
        s.save()
        s.flush()

        resp = self.app.get(url_for(controller='submission',
                                    action='edit',
                                    id=s.id))

        f = resp.form

        print "response:"
        print resp
        print "f.fields:"
        pprint.pprint(f.fields)

        # the value being returned is a string, from the form defaults
        self.assertEqual('3', f.fields['submission.type'][0].value)
        
        # clean up
        s.delete()
        s.flush()
