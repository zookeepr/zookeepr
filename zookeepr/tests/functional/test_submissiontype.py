# from zookeepr.model import SubmissionType, Role
# from zookeepr.tests.functional import *

# class TestSubmissionType(ControllerTest):
#     model = SubmissionType
#     name = 'submissiontype'
#     url = '/submissiontype'
#     samples = [dict(name='Paper'),
#                dict(name='BOF')]

#     def setUp(self):
#         super(ControllerTest, self).setUp()
#         self.log_in()
#         self.r = Role('site-admin')
#         self.p.roles.append(self.r)
#         self.r.save()
#         self.r.flush()

#     def tearDown(self):
#         self.r.delete()
#         self.r.flush()
#         self.log_out()
#         super(ControllerTest, self).tearDown()

#     def test_submission_view_lockdown(self):
#         # we got one person
#         #self.log_in()
#         # create roles
#         #r = Role('site-admin')
#         #r.save()
#         #r.flush()
#         # create a submission_type
#         st = SubmissionType('foo')
#         st.save()
#         st.flush()
#         # try to view the submission, we're not a site-admin
#         resp = self.app.get(url_for(controller='submissiontype',
#                                     action='view',
#                                     id=st.id),
#                             status=403)
#         # clean up
#         st.delete()
#         st.flush()
#         #r.delete()
#         #r.flush()
#         #self.log_out()
