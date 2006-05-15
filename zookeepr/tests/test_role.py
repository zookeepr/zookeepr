import unittest

from sqlalchemy import *

from zookeepr.models import *

class TestRoleModel(unittest.TestCase):

    def setUp(self):
        objectstore.clear()
    
    def test_create(self):
        """Test simple creation of a Role object"""

        # first let's assert that theres nothing in there
        rs = Role.select()
        self.failUnless(len(rs) == 0, "database is not empty")

        r = Role('site admin')
        objectstore.flush()

        self.assertEqual(r.name, 'site admin')

        # verify it's in the database
        rid = r.id

        r1 = Role.get(rid)

        self.assertEqual(r.name, r1.name)

        # clean up
        r.delete()
        r1.delete()
        objectstore.flush()

        # check
        rs = Role.select()
        self.assertEqual(len(rs), 0)

    def test_name_not_null(self):
        """Test that the name attribute of a role is not null"""

        r = Role()
        self.assertRaises(SQLError, objectstore.flush)
        objectstore.clear()
        
        # check
        rs = Role.select()
        self.assertEqual(len(rs), 0, "database was not left clean")
