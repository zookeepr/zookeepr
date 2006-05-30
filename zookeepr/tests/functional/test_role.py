from sqlalchemy import create_session

from zookeepr.tests import *
from zookeepr.models import *

class TestRoleController(TestController):
#     def test_index(self):
#         print
#         print "url for role is %s" % url_for(controller='role')
#         response = self.app.get(url_for(controller='role'))
#         # Test response...
#         print response

    def setUp(self):
        self.session = create_session()

    def tearDown(self):
        self.assertEqual([], self.session.query(Role).select())
        self.session.close()
        del self.session

    def test_create(self):
        """Test create action on /role"""

        ## create a new one
        u = url_for(controller='/role', action='new')
        # emulate first browser request
        res = self.app.get(u)
        print 'url for create is %s' % u
        res = self.app.post(u,
                            params={'role.name': 'admin'})

        # check that it's in the database
        rs = self.session.query(Role).select_by(name='admin')
        self.failIf(len(rs) == 0, "object not in database")
        self.failUnless(len(rs) == 1, "too many objects in database")
        r = rs[0]

        # clean up
        self.session.delete(r)
        self.session.flush()

    def test_edit(self):
        """Test edit operation on /role"""

        session = create_session()

        # create something in the db
        r = Role(name='admin')
        self.session.save(r)
        self.session.flush()
        rid = r.id
        self.session.clear()

        ## edit it
        u = url_for(controller='/role', action='edit', id=rid)
        res = self.app.get(u)
        
        res = self.app.post(u,
                            params={'role.name': 'speaker'})

        # check db
        r = self.session.get(Role, rid)
        self.assertEqual(r.name, "speaker")

        # clean up
        self.session.delete(r)
        self.session.flush()

        # check
        self.assertEqual([], self.session.query(Role).select())
        self.session.close()

    def test_delete(self):
        """Test delete operation on /role"""

        self.session = create_session()

        # create something
        r = Role(name='admin')
        self.session.save(r)
        self.session.flush()
        rid = r.id
        self.session.clear()

        ## delete it
        u = url_for(controller='/role', action='delete', id=rid)

        res = self.app.get(u)
        res = self.app.post(u)

        # check db
        r = self.session.get(Role, rid)
        self.failUnless(r is None, "object was not deleted")

        # check
        self.assertEqual([], self.session.query(Role).select())
        self.session.close()

    def test_invalid_get_on_edit(self):
        """Test that GET requests on role edit don't modify data"""
        # create some data
        r = Role(name='admin')
        self.session.save(r)
        self.session.flush()
        rid = r.id
        self.session.clear()

        u = url_for(controller='/role', action='edit', id=rid)
        res = self.app.get(u, params={'role.name':'feh'})

        # check db
        r = self.session.get(Role, rid)
        self.failUnless(r.name == 'admin')

        # clean up
        self.session.delete(r)
        self.session.flush()

    def test_invalid_get_on_delete(self):
        """Test that GET requests on role delete don't modify data"""
        # create some data
        r = Role(name='admin')
        self.session.save(r)
        self.session.flush()
        rid = r.id
        self.session.clear()

        u = url_for(controller='/role', action='delete', id=rid)
        res = self.app.get(u)
        # check
        self.session.get(Role, rid)
        self.failIf(r is None, "object was deleted")
        
        # clean up
        r = self.session.get(Role, rid)
        self.session.delete(r)
        self.session.flush()

    def test_invalid_get_on_new(self):
        """Test that GET requests on role new don't modify data"""

        # verify there's nothing in there
        self.assertEqual([], self.session.query(Role).select())
        
        u = url_for(controller='/role', action='new')
        res = self.app.get(u, params={'role.name': 'buzzn'})

    def test_invalid_delete(self):
        """Test delete of nonexistent roles is caught"""

        # verify there's nothing in there
        self.assertEqual([], self.session.query(Role).select())
        
        u = url_for(controller='/role', action='delete', id=1)
        res = self.app.post(u)

