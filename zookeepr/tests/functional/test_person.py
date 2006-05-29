from zookeepr.tests import *
from zookeepr.models import *

# class TestPersonController(TestController):
# #     def test_index(self):
# #         response = self.app.get(url_for(controller='person'))
# #         # Test response...
# #         response.mustcontain("person index")

#     def test_create(self):
#         """Test create action on /person"""

#         # create a new person
#         u = url_for(controller='/person', action='new')
#         params = {'person.handle': 'testguy',
#                   'person.email_address': 'testguy@example.org',
#                   'person.password': 'p4ssw0rd',
#                   'person.password_confirm': 'p4ssw0rd'}
#         res = self.app.post(u, params=params)

#         # check that it's in the dataase
#         ps = Person.select_by(handle='testguy')
#         self.failUnless(len(ps) == 1)
#         self.failUnless(ps[0].email_address == 'testguy@example.org')

#         # clean up
#         ps[0].delete()
#         objectstore.commit()
#         # check
#         ps = Person.select()
#         self.failUnless(len(ps) == 0, "database was not empty")

#     def test_edit(self):
#         """Test edit operation on /person"""

#         # create something in the db
#         p = Person(handle='testguy',
#                    email_address='testguy@example.org')
#         objectstore.commit()
#         pid = p.id

#         ## edit
#         u = url_for(controller='/person', action='edit', id='testguy')
#         params = {'person.email_address': 'zoinks@example.org'}
#         res = self.app.post(u, params=params)

#         # check DB
#         p = Person.get(pid)
#         self.failUnless(p.email_address == 'zoinks@example.org', "edit failed")

#         # clean up
#         p.delete()
#         objectstore.commit()
#         # check
#         ps = Person.select()
#         self.failUnless(len(ps) == 0)

#     def test_delete(self):
#         """Test delete operation on /person"""

#         # create something
#         p = Person(handle='testguy',
#                    email_address='testguy@example.org')
#         objectstore.commit()
#         pid = p.id

#         ## delete
#         u = url_for(controller='/person', action='delete', id='testguy')
#         res = self.app.post(u)

#         # check db
#         p = Person.get(pid)
#         self.failUnless(p is None, "object was not deleted")

#         # check
#         ps = Person.select()
#         self.failUnless(len(ps) == 0)

#     def test_edit_invalid_get(self):
#         """Test that GET requests on person edit are idempotent"""

#         # create some data
#         p = Person(handle='testguy',
#                    email_address='testguy@example.org')
#         objectstore.commit()
#         pid = p.id

#         u = url_for(controller='/person', action='edit', id='testguy')
#         params = {'person.email_address': 'testguy1@example.org'}
#         res = self.app.get(u, params=params)

#         p = Person.get(pid)
#         self.failUnless(p.email_address == 'testguy@example.org')

#         # clean up
#         p.delete()
#         objectstore.commit()
#         # check
#         ps = Person.select()
#         self.failUnless(len(ps) == 0)

#     def test_delete_invalid_get(self):
#         """Test that GET requests on person delete are idempotent"""

#         # create some data
#         p = Person(handle='testguy',
#                    email_address='testguy@example.org')
#         objectstore.commit()
#         pid = p.id

#         u = url_for(controller='/person', action='delete', id='testguy')
#         res = self.app.get(u)

#         p = Person.get(pid)
#         self.failIf(p is None)

#         # clean up
#         p.delete()
#         objectstore.commit()
#         # check
#         ps = Person.select()
#         self.failUnless(len(ps) == 0)

#     def test_create_invalid_get(self):
#         """Test that GET requests on person create are idempotent"""

#         u = url_for(controller='/person', action='new')
#         params = {'person.handle': 'testguy',
#                   'person.email_address': 'testguy@example.org'}
#         res = self.app.get(u, params=params)

#         # check DB
#         ps = Person.select()
#         self.failUnless(len(ps) == 0)

#     def test_delete_nonexistent(self):
#         """Test that delete action on nonexistent person is caught"""

#         ps = Person.select()
#         self.failUnless(len(ps) == 0, "database was not left empty")
        
#         u = url_for(controller='/person', action='delete', id='testguy')
#         res = self.app.post(u)

#         # check
#         ps = Person.select()
#         self.failUnless(len(ps) == 0, "database is not empty")
