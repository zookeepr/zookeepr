from zookeepr.tests.functional import *

class TestTalkController(ControllerTest):
    def test_talk_view(self):
        # set up
        pt = model.ProposalType(name='snuh')
        t = model.Proposal(title='foo',
                           abstract='bar',
                           )
        t.type = pt
        t.accepted = True
        self.dbsession.save(pt)
        self.dbsession.save(t)
        self.dbsession.flush()

        tid = t.id
        ptid = pt.id
        
        resp = self.app.get('/talk/%d' % t.id)

        resp.mustcontain("bar")
        resp.mustcontain("snuh")

        # clean up
        self.dbsession.delete(Query(model.Proposal).get(tid))
        self.dbsession.delete(Query(model.ProposalType).get(ptid))
        self.dbsession.flush()

    def test_talk_view_not_accepted(self):
        # set up
        pt = model.ProposalType(name='snuh')
        t = model.Proposal(title='foo',
                           abstract='bar',
                           )
        t.type = pt
        self.dbsession.save(pt)
        self.dbsession.save(t)
        self.dbsession.flush()

        tid = t.id
        ptid = pt.id
        
        resp = self.app.get('/talk/%d' % t.id, status=404)

        # clean up
        self.dbsession.delete(Query(model.Proposal).get(tid))
        self.dbsession.delete(Query(model.ProposalType).get(ptid))
        self.dbsession.flush()

