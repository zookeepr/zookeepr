from zookeepr.tests.model import *

class TestTalkDomainModel(ModelTest):
    def test_accepted_talk(self):
        # set up things
        t = model.ProposalType(name='snuh')
        self.dbsession.save(t)
        
        p1 = model.Proposal(title='a',
                            abstract='a',
                            )
        p1.accepted = False
        p1.type = t
        self.dbsession.save(p1)
        
        p2 = model.Proposal(title='b',
                            abstract='b',
                            )
        p2.accepted = True
        p2.type = t
        self.dbsession.save(p2)

        self.dbsession.flush()

        talks = self.dbsession.query(model.schedule.Talk).all()

        print "talks:", talks

        t1 = self.dbsession.query(model.schedule.Talk).get(p1.id)
        t2 = self.dbsession.query(model.schedule.Talk).get(p2.id)

        self.failUnless(t2 in talks, "t2 should be in talks")
        self.failIf(t1 in talks, "t1 shouldn't be in talks")

        # clean up
        self.dbsession.delete(p2)
        self.dbsession.delete(p1)
        self.dbsession.delete(t)
        self.dbsession.flush()

        # test cleanup
        self.failUnlessEqual([], self.dbsession.query(model.schedule.Talk).all())
