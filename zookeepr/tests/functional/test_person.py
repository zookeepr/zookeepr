from zookeepr.tests import *
from zookeepr.models import *

class TestPersonController(TestController):
#     def test_index(self):
#         response = self.app.get(url_for(controller='person'))
#         # Test response...
#         response.mustcontain("person index")

    def test_new(self):
        """Test basic operations on /person URL"""
        print

        # create a new person
        new_url = url_for(controller='/person', action='new')
        res = self.app.get(new_url)
        res.mustcontain("New person")
        res.mustcontain('Handle:')

        res = self.app.post(new_url,
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
        assert len(ps) == 1
        p = ps[0]

        pid = p.id

        ## edit
        ed_url = url_for(controller='/person', action='edit', id=pid)
        res = self.app.get(ed_url)
        res.mustcontain('Edit person')
        res.mustcontain('Handle:')
        res = self.app.post(ed_url,
                            params=dict(email_address='zoinks@example.org'))

        # follow redirect, check it's the list page
        res = res.follow()
        res.mustcontain('List persons')

        # check DB
        p = Person.get(pid)
        self.failUnless(p.email_address == 'zoinks@example.org')

        ## delete
        del_url = url_for(controller='/person', action='delete', id=pid)
        res = self.app.get(del_url)
        res.mustcontain('Delete person')
        res = self.app.post(del_url, params=dict(delete='ok'))
        res = res.follow()
        res.mustcontain("List")
        # check db
        p = Person.get(pid)
        self.failUnless(p is None)

        # check
        ps = Person.select()
        assert len(ps) == 0
