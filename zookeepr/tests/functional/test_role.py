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
        rs = session.query(model.Role).select_by(name='admin')
        self.failIf(len(rs) == 0, "object not in database")
        self.failUnless(len(rs) == 1, "too many objects in database")
        r = rs[0]

        # clean up
        r.delete()
        objectstore.commit()
        # check
        rs = Role.select()
        self.failUnless(len(rs) == 0, "database is not empty")

    def test_edit(self):
        """Test edit operation on /role"""

        # create something in the db
        r = Role(name='admin')
        objectstore.commit()
        rid = r.id

        ## edit it
        u = url_for(controller='/role', action='edit', id=rid)
        res = self.app.get(u)
        
        res = self.app.post(u,
                            params={'role.name': 'speaker'})

        # check db
        r = Role.get(rid)
        self.assertEqual(r.name, "speaker")

        # clean up
        r.delete()
        objectstore.commit()
        # check
        rs = Role.select()
        print 'remaining in db: %s' % rs
        self.failUnless(len(rs) == 0, "database is not empty")

    def test_delete(self):
        """Test delete operation on /role"""

        # create something
        r = Role(name='admin')
        objectstore.commit()
        rid = r.id

        ## delete it
        u = url_for(controller='/role', action='delete', id=rid)

        res = self.app.get(u)
        res = self.app.post(u)

        # check db
        r = Role.get(rid)
        self.failUnless(r is None, "object was not deleted")
        # check
        rs = Role.select()
        self.failUnless(len(rs) == 0, "database is not empty")

    def test_invalid_get_on_edit(self):
        """Test that GET requests on role edit don't modify data"""
        # create some data
        r = Role(name='admin')
        objectstore.commit()
        rid = r.id

        u = url_for(controller='/role', action='edit', id=rid)
        res = self.app.get(u, params={'role.name':'feh'})

        # check db
        r = Role.get(rid)
        self.failUnless(r.name == 'admin')

        # clean up
        r.delete()
        objectstore.commit()
        # doublecheck
        rs = Role.select()
        self.failUnless(len(rs) == 0, "dtabase is not empty")

    def test_invalid_get_on_delete(self):
        """Test that GET requests on role delete don't modify data"""
        # create some data
        r = Role(name='admin')
        objectstore.commit()
        rid = r.id

        u = url_for(controller='/role', action='delete', id=rid)
        res = self.app.get(u)
        # check
        r = Role.get(rid)
        self.failIf(r is None, "object was deleted")
        
        # clean up
        r.delete()
        objectstore.commit()
        # doublecheck
        rs = Role.select()
        self.failUnless(len(rs) == 0, "database is not empty")

    def test_invalid_get_on_new(self):
        """Test that GET requests on role new don't modify data"""

        # verify there's nothing in there
        rs = Role.select()
        self.failUnless(len(rs) == 0, "database was not empty")
        
        u = url_for(controller='/role', action='new')
        res = self.app.get(u, params={'role.name': 'buzzn'})
        # check
        rs = Role.select()
        self.failUnless(len(rs) == 0, "database is not empty")

    def test_invalid_delete(self):
        """Test delete of nonexistent roles is caught"""

        # make sure there's nothing in there
        rs = Role.select()
        self.failUnless(len(rs) == 0, "database was not empty")
        
        u = url_for(controller='/role', action='delete', id=1)
        res = self.app.post(u)

        # check
        rs = Role.select()
        self.failUnless(len(rs) == 0, "database is not empty")
