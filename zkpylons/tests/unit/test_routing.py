import unittest

from zkpylons.config.routing import make_map
from routes import url_for, request_config

class TestRouting(unittest.TestCase):
    def setUp(self):
        # Set up a local state because we aren't sure what has been shoveled into the shared one
        class Obby(object): pass
        myobj = Obby()
        class Callable(object):
            def __call__(self):
                return myobj
        
        request_config().request_local = Callable() 

        config = {
            'pylons.paths' : { 'controllers' : None },
            'debug' : True,
        }
        self.map = make_map(config)

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

    def test_home_routing(self):
        """Test the routing of the home controller"""
        self.assertEqual(dict(controller='home',
                              action='index'),
                         self.map.match('/'))

    def test_home_named_route(self):
        self.assertEqual('/',
                         url_for('home'))

