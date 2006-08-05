from zookeepr.tests.functional import *

class TestSubmission(ControllerTest):
    model = model.Submission
    name = 'submission'
    url = '/submission'
    samples = [dict(title='test',
                    abstract='abstract 1',
                    experience='experience 1',
                    url='http://example.org',
                    submission_type_id=1,
                    ),
               dict(title='not a test',
                    abstract='abstract 2',
                    experience='experience 2',
                    submission_type_id=2,
                    url='http://lca2007.linux.org.au',
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

    def test_selected_radio_button_in_edit(self):
        # Test that a radio button is checked when editing a submission
        s = model.Submission(id=1,
                             submission_type_id=3,
                             title='foo',
                             abstract='bar',
                             experience='',
                             url='')
        self.session.save(s)
        self.session.flush()

        resp = self.app.get(url_for(controller='submission',
                                    action='edit',
                                    id=s.id))

        f = resp.form

        # the value being returned is a string, from the form defaults
        self.assertEqual('3', f.fields['submission.submission_type_id'][0].value)
        
        # clean up
        self.session.delete(s)
        self.session.flush()
