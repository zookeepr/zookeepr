from zookeepr.tests.model import *

class TestRoleModel(ModelTest):
    model = 'Role'
    attrs = dict(name='site admin')
    not_null = ['name']

    def test_create(self):
        self.create()

    def test_not_nullable(self):
        self.not_nullable()

    def test_map_person(self):
        """Test mapping persons to roles"""

        p = model.Person(handle='testguy',
                         email_address='testguy@example.org')
        r = model.Role('admin')
        p.roles.append(r)
        objectstore.flush()

        self.assertEqual(['admin'], [r.name for r in p.roles])

        # clean up
        p.delete()
        r.delete()
        objectstore.flush()
        # check
        self.assertEqual(len(model.Role.select()), 0)
        self.assertEqual(len(model.Person.select()), 0)
