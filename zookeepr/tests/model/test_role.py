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

         p = model.Person(handle='testguy',
                          email_address='testguy@example.org')
         r = model.Role('admin')
         
         session.save(p)
         session.save(r)
         
         p.roles.append(r)

         session.flush()
         
         rid = r.id
         pid = p.id
         
         session.clear()
         
         p = session.get(model.Person, pid)
         self.assertEqual(['admin'], [r.name for r in p.roles])
         
         # clean up
         session.delete(p)
         session.delete(session.get(model.Role, rid))
         session.flush()
         
         # check
         self.assertEqual(0, len(session.query(model.Role).select()))
         self.check_empty_session()
