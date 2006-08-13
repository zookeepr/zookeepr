from zookeepr.model import SubmissionType
from zookeepr.tests.functional import *

class TestSubmissionType(ControllerTest):
    model = SubmissionType
    name = 'submissiontype'
    url = '/submissiontype'
    samples = [dict(name='Paper'),
               dict(name='BOF')]

    def test_submission_view_lockdown(self):
        # we got one person
        self.log_in()
        # create a submission_type
        st = SubmissionType('foo')
        st.save()
        st.flush()
        # try to view the submission, we're not a site-admin
        resp = self.app.get(url_for(controller='submissiontype',
                                    action='view',
                                    id=st.id),
                            status=403)
        # clean up
        st.delete()
        st.flush()
        self.log_out()
