import md5

from zookeepr.tests.model import *

class TestCFP(ModelTest):

    def test_create(self):
        session = create_session()

        reg = model.Registration(email_address='testguy@example.org',
                                 password='password',
                           )

        sub = model.Submission(title="title",
                               abstract="abstract",
                               )

        reg.submissions.append(sub)

        session.save(reg)
        session.save(sub)

        session.flush()
