from zookeepr.model import Person, Role
from zookeepr.tests.model import *

class TestRoleModel(ModelTest):
     model = 'Role'
     samples = [dict(name='site admin'),
                dict(name='speaker'),
                ]
     not_nullables = ['name']
     uniques = ['name']

     def test_map_person(self):
         """Test mapping persons to roles"""
         session = create_session()

         p = Person(handle='testguy',
                    email_address='testguy@example.org')
         r = Role('admin')

         p.save()
         r.save()
         p.flush()
         r.flush()
         
         p.roles.append(r)

         p.save()
         p.flush()
         
         rid = r.id
         pid = p.id
         
         objectstore.clear()
         
         p = Person.get(pid)
         self.assertEqual(['admin'], [r.name for r in p.roles])
         
         # clean up
         p.delete()
         p.flush()
         Role.get(rid).delete()
         Role.get(rid).flush()
         
         # check
         self.assertEqual(0, len(Role.select()))
         self.check_empty_session()
