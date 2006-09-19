from zookeepr.model import Person, Role
from zookeepr.tests.model import *

class TestRoleModel(ModelTest):
     domain = model.core.Role

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

         objectstore.save(p)
         objectstore.save(r)
         p.roles.append(r)
         objectstore.flush()

         rid = r.id
         pid = p.id
         
         objectstore.clear()

         p = objectstore.get(Person, pid)
         r = objectstore.get(Role, rid)
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
         objectstore.delete(p)
         objectstore.delete(r)
         objectstore.flush()
         
         # check
         self.assertEqual(0, len(objectstore.query(Role).select()))
         self.check_empty_session()

     def test_many_roles(self):
         p1 = Person(email_address='one@example.org', password='1')
         p2 = Person(email_address='two@example.org', password='2')
         p3 = Person(email_address='three@example.org', password='3')
         p4 = Person(email_address='four@example.org', password='4')
         objectstore.save(p1)
         objectstore.save(p2)
         objectstore.save(p3)
         objectstore.save(p4)

         r1 = Role('single')
         r2 = Role('double')
         objectstore.save(r1)
         objectstore.save(r2)

         p1.roles.append(r1)
         p2.roles.append(r2)
         p4.roles.append(r2)

         objectstore.flush()
         
         p = (p1.id, p2.id, p3.id, p4.id)
         r = (r1.id, r2.id)

         objectstore.clear()

         p1 = objectstore.get(Person, p[0])
         p2 = objectstore.get(Person, p[1])
         p3 = objectstore.get(Person, p[2])
         p4 = objectstore.get(Person, p[3])
         r1 = objectstore.get(Role, r[0])
         r2 = objectstore.get(Role, r[1])

         # test
         self.failUnless(r1 in p1.roles)
         self.failUnless(r2 in p2.roles)
         self.failUnless(r2 in p4.roles)
         self.assertEqual([], p3.roles)

         self.failIf(r1 in p2.roles)
         self.failIf(r1 in p3.roles)
         self.failIf(r1 in p4.roles)

         self.failIf(r2 in p1.roles)
         self.failIf(r2 in p3.roles)

         # clean up
         objectstore.delete(p1)
         objectstore.delete(p2)
         objectstore.delete(p3)
         objectstore.delete(p4)
         objectstore.delete(r1)
         objectstore.delete(r2)

         objectstore.flush()
