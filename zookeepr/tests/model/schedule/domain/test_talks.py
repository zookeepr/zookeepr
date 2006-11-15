from zookeepr.tests.model import *

class TestTalkDomainModel(ModelTest):
    def test_accepted_talk(self):
        # set up things
        t = model.ProposalType(name='snuh')
        objectstore.save(t)
        
        p1 = model.Proposal(title='a',
                            abstract='a',
                            )
        p1.accepted = False
        p1.type = t
        objectstore.save(p1)
        
        p2 = model.Proposal(title='b',
                            abstract='b',
                            )
        p2.accepted = True
        p2.type = t
        objectstore.save(p2)

        talks = Query(model.schedule.Talk).select()

        self.failIf(p1 in talks, "p1 shouldn't be in talks")
        self.failUnless(p2 in talks, "p2 should be in talks")

        # clean up
        objectstore.delete(p2)
        objectstore.delete(p1)
        objectstore.delete(t)
        objectstore.flush()

        # test cleanup
        self.failUnlessEqual([], Query(model.schedule.Talk).select())
