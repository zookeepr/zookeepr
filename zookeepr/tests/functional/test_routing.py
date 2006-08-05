import unittest

from zookeepr.config.routing import make_map
from zookeepr.tests.functional import url_for

class TestRouting(unittest.TestCase):
    def setUp(self):
        self.map = make_map()

    def test_default_controller_url(self):
        self.assertEqual('/c',
                        url_for(controller='c'))

    def test_default_controller_index_url(self):
        self.assertEqual('/c',
                         url_for(controller='c', action='index'))

    def test_default_controller_new_url(self):
        self.assertEqual('/c/new',
                         url_for(controller='c', action='new'))

    def test_default_controller_view_url(self):
        self.assertEqual('/c/1',
                         url_for(controller='c', action='view', id=1))

    def test_default_controller_action_url(self):
        for action in ['edit', 'update', 'delete']:
            self.assertEqual('/c/1/%s' % action,
                             url_for(controller='c', action=action, id=1))

    def test_about_controller_id_url(self):
        self.assertEqual('/about/programme',
                         url_for(controller='about',
                                 action='view',
                                 id='programme'))

    def test_home_routing(self):
        """Test the routing of the home controller"""
        self.assertEqual(dict(controller='home',
                              action='index'),
                         self.map.match('/'))

    def test_home_named_route(self):
        self.assertEqual('/',
                         url_for('home'))

    def test_cfp_routing(self):
        """test the routing of the cfp urls"""
        self.assertEqual(dict(controller='cfp',
                              action='index'),
                         self.map.match('/cfp'))

    def test_cfp_named_route(self):
        self.assertEqual('/cfp',
                         url_for('cfp'))

    def test_cfp_submission_url(self):
        """test the routing of the cfp submit url"""
        self.assertEqual(dict(controller='cfp',
                              action='submit'),
                         self.map.match('/cfp/submit'))

    def test_cfp_submission_named_route(self):
        submit_cfp = url_for('submit_cfp')
        self.assertEqual('/cfp/submit',
                         submit_cfp)

    def test_registration_confirmation_url(self):
        """test the routing of the registration confirmation url"""
        self.assertEqual(dict(controller='register',
                              action='confirm',
                              id='N'),
                         self.map.match('/register/confirm/N'))

    def test_registratrion_confirmation_named_route(self):
        reg_confirm = url_for('reg_confirm', id='N')
        self.assertEqual('/register/confirm/N',
                         reg_confirm)

    def test_cfp_thankyou_routing(self):
        u = '/cfp/thankyou'
        self.assertEqual(dict(controller='cfp',
                              action='thankyou',
                              ),
                         self.map.match(u))
