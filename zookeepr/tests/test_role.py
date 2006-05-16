import unittest

from sqlalchemy import *

from zookeepr.models import *

class TestRoleModel(unittest.TestCase):

    def setUp(self):
        objectstore.clear()
    
    def test_create(self):
        """Test simple creation of a Role object"""

        # first let's assert that theres nothing in there
        self.assertEqual(len(Role.select()), 0)

        # create
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
        self.assertEqual(len(Role.select()), 0)

    def test_name_not_null(self):
        """Test that the name attribute of a role is not null"""

        r = Role()
        self.assertRaises(SQLError, objectstore.flush)
        objectstore.clear()
        
        # check
        self.assertEqual(len(Role.select()), 0)

    def test_map_person(self):
        """Test mapping persons to roles"""

        p = Person(handle='testguy',
                   email_address='testguy@example.org')
        r = Role('admin')
        p.roles.append(r)
        objectstore.flush()

        self.assertEqual(['admin'], [r.name for r in p.roles])

        # clean up
        p.delete()
        r.delete()
        objectstore.flush()
        # check
        self.assertEqual(len(Role.select()), 0)
        self.assertEqual(len(Person.select()), 0)
