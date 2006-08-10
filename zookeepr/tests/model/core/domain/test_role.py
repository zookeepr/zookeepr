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

         p = Person(handle='testguy',
                    email_address='testguy@example.org')
         r = Role('admin')

         p.save()
         p.flush()

         r.save()
         r.flush()
         
         p.roles.append(r)

         print "pre clear, p.roles:", p.roles

         p.save()
         p.flush()

         print "p saved:", p
         
         rid = r.id
         pid = p.id
         
         objectstore.clear()

         print "pre get p:", p
         
         p = Person.get(pid)
         r = Role.get(rid)
         print "new p:", p
         print "p.roles:", p.roles

         print "r:", r
         print "r:", r.people

         print "p.roles:", [id(x) for x in p.roles]
         print "r:", id(r)

         self.failUnless(r in p.roles, "%r not in p.roles (currently %r)" % (r, p.roles))

         # test people
         self.failUnless(p in r.people, "%r not in r.people (currently %r)" % (p, r.people))
         
         # clean up
         p.delete()
         p.flush()
         Role.get(rid).delete()
         Role.get(rid).flush()
         
         # check
         self.assertEqual(0, len(Role.select()))
         self.check_empty_session()
