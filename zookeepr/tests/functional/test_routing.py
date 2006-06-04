from zookeepr.tests.functional import *

class TestRouting(ControllerTest):
    def test_routing(self):
        """Test url routing"""

        ctlr = '/ctlr'
        # print to clear output when running verbose
        print
        
        # controller w/o action or id
        u = url_for(controller=ctlr)
        print "base controller url: %s" % u
        self.failUnless(u == ctlr)

        # controller w/ index action
        u = url_for(controller=ctlr, action='index')
        print "index action url: %s" % u
        self.failUnless(u == ctlr)
        
        # controller w/ new action
        u = url_for(controller=ctlr, action='new')
        print "new action url: %s" % u
        self.failUnless(u == ctlr + '/new')

        # controller w/ view action
        u = url_for(controller=ctlr, action='view', id=1)
        print "view action url: %s" % u
        self.failUnless(u == ctlr + '/1')

        # controller w/ other actions and id
        for action in ['edit', 'update', 'delete']:
            u = url_for(controller=ctlr, action=action, id=1)
            print "%s action url: %s" % (action, u)
            self.failUnless(u == ctlr + '/1/%s' % action)

    def test_about(self):
        """Test the about sub-url"""

        ctlr = '/about'
        
        print
        u = url_for(controller=ctlr, action='view', id='programme')
        print "programme url:", u
        self.assertEqual(ctlr + '/programme', u)
        
