from zookeepr.tests.model import *

class TestRoleModel(CRUDModelTest):
     domain = model.core.Role

     samples = [dict(name='site admin'),
                dict(name='speaker'),
                ]
# FIXME: chckec
     not_nullables = ['name']
     uniques = ['name']

     def test_map_person(self):
         """Test mapping persons to roles"""

         p = model.Person(handle='testguy',
                    email_address='testguy@example.org')
         r = model.Role('admin')

         self.dbsession.save(p)
         self.dbsession.save(r)
         p.roles.append(r)
         self.dbsession.flush()

         rid = r.id
         pid = p.id
         
         self.dbsession.clear()

         p = self.dbsession.get(model.Person, pid)
         r = self.dbsession.get(model.Role, rid)
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
         self.dbsession.delete(p)
         self.dbsession.delete(r)
         self.dbsession.flush()
         
         # check
         self.assertEqual(0, len(self.dbsession.query(model.Role).select()))
         self.check_empty_session()

     def test_many_roles(self):
         p1 = model.Person(email_address='one@example.org', password='1')
         p2 = model.Person(email_address='two@example.org', password='2')
         p3 = model.Person(email_address='three@example.org', password='3')
         p4 = model.Person(email_address='four@example.org', password='4')
         self.dbsession.save(p1)
         self.dbsession.save(p2)
         self.dbsession.save(p3)
         self.dbsession.save(p4)

         r1 = model.Role('single')
         r2 = model.Role('double')
         self.dbsession.save(r1)
         self.dbsession.save(r2)

         p1.roles.append(r1)
         p2.roles.append(r2)
         p4.roles.append(r2)

         self.dbsession.flush()
         
         p = (p1.id, p2.id, p3.id, p4.id)
         r = (r1.id, r2.id)

         self.dbsession.clear()

         p1 = self.dbsession.get(model.Person, p[0])
         p2 = self.dbsession.get(model.Person, p[1])
         p3 = self.dbsession.get(model.Person, p[2])
         p4 = self.dbsession.get(model.Person, p[3])
         r1 = self.dbsession.get(model.Role, r[0])
         r2 = self.dbsession.get(model.Role, r[1])

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
         self.dbsession.delete(p1)
         self.dbsession.delete(p2)
         self.dbsession.delete(p3)
         self.dbsession.delete(p4)
         self.dbsession.delete(r1)
         self.dbsession.delete(r2)

         self.dbsession.flush()
