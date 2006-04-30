from zookeepr.tests import *
from zookeepr.models import *

class TestPersonController(TestController):
#     def test_index(self):
#         response = self.app.get(url_for(controller='person'))
#         # Test response...
#         response.mustcontain("person index")

    def test_new(self):
        """Test basic creation operation on /person URL"""
        print

        # create a new person
        u = url_for(controller='/person', action='new')
        res = self.app.get(u)
        res.mustcontain("New person")
        res.mustcontain('Handle:')

        res = self.app.post(u,
                            params=dict(handle='testguy',
                                        email_address='testguy@example.org'))

        # follow redirect
        res = res.follow()
        # check we're viewing the right page
        res.mustcontain('View person')
        res.mustcontain('Handle:')
        res.mustcontain('testguy')

        # check that it's in the dataase
        ps = Person.select_by(handle='testguy')
        self.failUnless(len(ps) == 1)
        self.failUnless(ps[0].email_address == 'testguy@example.org')

        # clean up
        ps[0].delete()
        objectstore.commit()
        # check
        ps = Person.select()
        self.failUnless(len(ps) == 0)

    def test_edit(self):
        """Test basic edit operation on /person URL"""
        print

        # create something in the db
        p = Person(handle='testguy',
                   email_address='testguy@example.org')
        objectstore.commit()
        pid = p.id

        ## edit
        u = url_for(controller='/person', action='edit', id='testguy')
        print "ed_url is %s" % u
        res = self.app.get(u)
        res.mustcontain('Edit person')
        res.mustcontain('Handle:')
        res = self.app.post(u,
                            params=dict(email_address='zoinks@example.org'))

        # follow redirect, check it's the list page
        res = res.follow()
        res.mustcontain('List persons')

        # check DB
        p = Person.get(pid)
        self.failUnless(p.email_address == 'zoinks@example.org')

        # clean up
        p.delete()
        objectstore.commit()
        # check
        ps = Person.select()
        self.failUnless(len(ps) == 0)

    def test_delete(self):
        """Test basic delete operation on /person URL"""
        print

        # create something
        p = Person(handle='testguy',
                   email_address='testguy@example.org')
        objectstore.commit()
        pid = p.id

        ## delete
        u = url_for(controller='/person', action='delete', id='testguy')
        res = self.app.get(u)
        res.mustcontain('Delete person')
        res = self.app.post(u, params=dict(delete='ok'))
        res = res.follow()
        res.mustcontain("List")
        # check db
        p = Person.get(pid)
        self.failUnless(p is None)

        # check
        ps = Person.select()
        self.failUnless(len(ps) == 0)

    def setUp(self):
        objectstore.clear()
