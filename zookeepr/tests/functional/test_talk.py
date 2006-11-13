from zookeepr.tests.functional import *

class TestTalkController(ControllerTest):
    def test_talk_view(self):
        # set up
        pt = model.ProposalType(name='snuh')
        t = model.Proposal(title='foo',
                           abstract='bar',
                           )
        t.type = pt
        objectstore.save(pt)
        objectstore.save(t)
        objectstore.flush()
        
        resp = self.app.get('/talk/%d' % t.id)

        resp.mustcontain("bar")
        resp.mustcontain("snuh")

        # clean up
        objectstore.delete(t)
        objectstore.delete(pt)
        objectstore.flush()

