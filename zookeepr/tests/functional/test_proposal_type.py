# from zookeepr.model import ProposalType, Role
# from zookeepr.tests.functional import *

# class TestProposalType(CRUDControllerTest):
#     model = ProposalType
#     name = 'proposal_type'
#     url = '/proposal_type'
#     samples = [dict(name='Paper'),
#                dict(name='BOF')]

#     def setUp(self):
#         super(CRUDControllerTest, self).setUp()
#         self.log_in()
#         self.r = Role('site-admin')
#         self.p.roles.append(self.r)
#         self.r.save()
#         self.r.flush()

#     def tearDown(self):
#         self.r.delete()
#         self.r.flush()
#         self.log_out()
#         super(CRUDControllerTest, self).tearDown()

#     def test_proposal_view_lockdown(self):
#         # we got one person
#         #self.log_in()
#         # create roles
#         #r = Role('site-admin')
#         #r.save()
#         #r.flush()
#         # create a proposal_type
#         st = ProposalType('foo')
#         st.save()
#         st.flush()
#         # try to view the proposal, we're not a site-admin
#         resp = self.app.get(url_for(controller='proposal_type',
#                                     action='view',
#                                     id=st.id),
#                             status=403)
#         # clean up
#         st.delete()
#         st.flush()
#         #r.delete()
#         #r.flush()
#         #self.log_out()
