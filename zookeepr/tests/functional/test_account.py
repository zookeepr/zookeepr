import datetime

from zookeepr.model import Person
from zookeepr.tests.functional import *

class TestAccountController(ControllerTest):
    
#     def test_account_signin_routing(self):
#         self.assertEqual(dict(controller='account',
#                               action='signin'),
#                          self.map.match('/account/signin'))

#     def test_account_signin_url(self):
#         self.assertEqual('/account/signin',
#                          url_for(controller='account', action='signin'))

#     def test_account_signout_url(self):
#         self.assertEqual('/account/signout',
#                          url_for(controller='account', action='signout'))

    def test_signin_signout(self):
        """Test account sign in"""
        # create a user
        p = model.core.Person(email_address='testguy@example.org',
                         password='p4ssw0rd')
        p.activated = True

        self.objectstore.save(p)
        self.objectstore.flush()
        
        # try to log in
        resp = self.app.get(url_for(controller='account',
                                    action='signin'))
        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f['password'] = 'p4ssw0rd'
        resp = f.submit()

        self.failUnless('person_id' in resp.session)
        self.assertEqual(p.id,
                         resp.session['person_id'])

        # sign out
        resp = resp.goto(url_for(controller='account',
                                 action='signout'))

        print "resp.session", resp.session

        self.failIf('contact_id' in resp.session)
        
        # clean up
        self.objectstore.delete(p)
        self.objectstore.flush()

    def test_signin_invalid(self):
        """Test invalid login details"""
        # login
        resp = self.app.get(url_for(controller='/account', action='signin'))
        f = resp.form
        f['email_address'] = 'testguy'
        f['password'] = 'password'

        f.submit()

        self.failIf('contact_id' in resp.session)

    def test_signin_unconfirmed(self):
        # create an account
        p = model.core.Person(email_address='testguy@example.org',
                         password='p4ssw0rd')
        self.objectstore.save(p)
        self.objectstore.flush()
        
        # try to login
        resp = self.app.get(url_for(controller='account',
                                    action='signin'))
        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f['password'] = 'p4ssw0rd'
        resp = f.submit()
    
        # test that login is refused
        self.failIf('person_id' in resp.session)
        
        # clean up
        self.objectstore.delete(p)
        self.objectstore.flush()

    def test_registration_confirmation(self):
        # insert registration model object
        timestamp = datetime.datetime.now()
        email_address = 'testguy@testguy.org'
        password = 'password'
        r = Person(creation_timestamp=timestamp,
                   email_address=email_address,
                   password=password,
                   activated=False)
        url_hash = r.url_hash
        print url_hash
        self.objectstore.save(r)
        self.objectstore.flush()
        rid = r.id
        print r
        # clear so that we reload the object later
        self.objectstore.clear()
        
        # visit the link
        response = self.app.get('/account/confirm/' + url_hash)
        response.mustcontain('Thanks for confirming your registration')
        
        # test that it's activated
        r = self.objectstore.get(Person,rid)
        self.assertEqual(True, r.activated, "registration was not activated")

        # clean up
        self.objectstore.delete(self.objectstore.get(Person, rid))
        self.objectstore.flush()

    def test_registration_confirmation_invalid_url_hash(self):
        """test that an invalid has doesn't activate anything"""
        self.assertEmptyModel(Person)

        response = self.app.get('/account/confirm/nonexistent', status=404)
