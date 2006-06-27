import unittest

from zookeepr.config.routing import make_map
from zookeepr.tests.functional import url_for

class TestRouting(unittest.TestCase):
    def setUp(self):
        self.map = make_map()

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
        

    def test_home_routing(self):
        """Test the routing of the home controller"""
        u = '/'
        self.assertEqual(dict(controller='home',
                              action='index'),
                         self.map.match(u))

    def test_cfp_routing(self):
        """test the routing of the cfp urls"""
        u = '/cfp'
        self.assertEqual(dict(controller='cfp',
                              action='index'),
                         self.map.match(u))

        cfp = url_for('cfp')
        self.assertEqual(u, cfp)

    def test_cfp_submission_url(self):
        """test the routing of the cfp submit url"""

        # test the mapper
        u = '/cfp/submit'
        self.assertEqual(dict(controller='cfp',
                              action='submit'),
                         self.map.match(u))

        # test the named route
        submit_cfp = url_for('submit_cfp')
        self.assertEqual(u, submit_cfp)

    def test_registration_confirmation_url(self):
        """test the routing of the registration confirmation url"""
        u = '/register/confirm/N'
        self.assertEqual(dict(controller='register',
                              action='confirm',
                              id='N'),
                         self.map.match(u))

        # test the named route
        reg_confirm = url_for('reg_confirm', id='N')
        self.assertEqual(u, reg_confirm)
