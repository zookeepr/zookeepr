#import md5
#
#from zookeepr.tests.model import *
#
#class TestCFP(ModelTest):
#
#    def test_create(self):
#        session = create_session()
#
#        reg = model.core.domain.Registration(email_address='testguy@example.org',
#                                 password='password',
#                           )
#
#        sub = model.submission.domain.Submission(title="title",
#                               abstract="abstract",
#                               )
#
#        session.save(reg)
#        session.save(sub)
#
#        reg.submissions.append(sub)
#
#        session.flush()
#
#
#        # clean up
#        session.delete(sub)
#        session.delete(reg)
#        session.flush()
#
