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

        objectstore.flush()

        talks = Query(model.schedule.Talk).select()

        print "talks:", talks

        t1 = Query(model.schedule.Talk).get(p1.id)
        t2 = Query(model.schedule.Talk).get(p2.id)

        self.failUnless(t2 in talks, "t2 should be in talks")
        self.failIf(t1 in talks, "t1 shouldn't be in talks")

        # clean up
        objectstore.delete(p2)
        objectstore.delete(p1)
        objectstore.delete(t)
        objectstore.flush()

        # test cleanup
        self.failUnlessEqual([], Query(model.schedule.Talk).select())
