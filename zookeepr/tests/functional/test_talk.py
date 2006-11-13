from zookeepr.tests.functional import *

class TestTalkController(ControllerTest):
    def test_talk_view(self):
        # set up
        t = model.Proposal(title='foo',
                           abstract='bar',
                           )
        objectstore.save(t)
        objectstore.flush()
        
        resp = self.app.get('/talk/%d' % t.id)

        resp.mustcontain("bar")

        # clean up
        objectstore.delete(t)
        objectstore.flush()

