from zookeepr.tests.functional import *

class TestTalkController(CRUDControllerTest):
    def test_talk_view(self):
        # set up
        pt = model.ProposalType(name='snuh')
        t = model.Proposal(title='foo',
                           abstract='bar',
                           )
        t.type = pt
        t.accepted = True
        objectstore.save(pt)
        objectstore.save(t)
        objectstore.flush()

        tid = t.id
        ptid = pt.id
        
        resp = self.app.get('/talk/%d' % t.id)

        resp.mustcontain("bar")
        resp.mustcontain("snuh")

        # clean up
        objectstore.delete(Query(model.Proposal).get(tid))
        objectstore.delete(Query(model.ProposalType).get(ptid))
        objectstore.flush()

    def test_talk_view_not_accepted(self):
        # set up
        pt = model.ProposalType(name='snuh')
        t = model.Proposal(title='foo',
                           abstract='bar',
                           )
        t.type = pt
        objectstore.save(pt)
        objectstore.save(t)
        objectstore.flush()

        tid = t.id
        ptid = pt.id
        
        resp = self.app.get('/talk/%d' % t.id, status=404)

        # clean up
        objectstore.delete(Query(model.Proposal).get(tid))
        objectstore.delete(Query(model.ProposalType).get(ptid))
        objectstore.flush()

