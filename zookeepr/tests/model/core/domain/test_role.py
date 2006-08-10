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

     def test_many_roles(self):
         p1 = Person(email_address='one@example.org', password='1')
         p1.save()
         p2 = Person(email_address='two@example.org', password='2')
         p2.save()
         p3 = Person(email_address='three@example.org', password='3')
         p3.save()
         p4 = Person(email_address='four@example.org', password='4')
         p4.save()

         r1 = Role('single')
         r1.save()
         r1.flush()
         r2 = Role('double')
         r2.save()
         r2.flush()

         p1.roles.append(r1)
         p2.roles.append(r2)
         p4.roles.append(r2)

         objectstore.flush()
         p = (p1.id, p2.id, p3.id, p4.id)
         r = (r1.id, r2.id)

         objectstore.clear()

         p1 = Person.get(p[0])
         p2 = Person.get(p[1])
         p3 = Person.get(p[2])
         p4 = Person.get(p[3])
         r1 = Role.get(r[0])
         r2 = Role.get(r[1])

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
         p1.delete()
         p2.delete()
         p3.delete()
         p4.delete()

         r1.delete()
         r2.delete()

         objectstore.flush()
