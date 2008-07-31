import datetime
import md5
import re

from paste.fixture import Dummy_smtplib

from zookeepr.model import Person, PasswordResetConfirmation
from zookeepr.tests.functional import *

class TestPersonController(ControllerTest):

    def test_registration_confirmation_url(self):
        """test the routing of the registration confirmation url"""
        self.assertEqual(dict(controller='person',
                              action='confirm',
                              confirm_hash='N'),
                         self.map.match('/person/confirm/N'))

    def test_registratrion_confirmation_named_route(self):
        reg_confirm = url_for('acct_confirm', confirm_hash='N')
        self.assertEqual('/person/confirm/N',
                         reg_confirm)

    def test_person_signin_routing(self):
        self.assertEqual(dict(controller='person',
                              action='signin'),
                         self.map.match('/person/signin'))
        
    def test_person_signin_url(self):
        self.assertEqual('/person/signin',
                         url_for(controller='person', action='signin', id=None))

    def test_person_signout_url(self):
        self.assertEqual('/person/signout',
                         url_for(controller='person', action='signout', id=None))

    def assertSignedIn(self, session, id):
        self.failUnless('signed_in_person_id' in session)
        self.assertEqual(id, session['signed_in_person_id'])

    def test_signin_signout(self):
        """Test person sign in"""
        # create a user
        p = model.core.Person(email_address='testguy@example.org',
                         password='p4ssw0rd',
			 handle='testguy')
        p.activated = True

        self.dbsession.save(p)
        self.dbsession.flush()
        
        # try to log in
        resp = self.app.get(url_for(controller='person',
                                    action='signin'))
        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f['password'] = 'p4ssw0rd'
        resp = f.submit()

        self.assertSignedIn(resp.session, p.id)

        # see if we're still logged in when we go to another page
        resp = self.app.get(url_for(controller='home', action='view'))

        self.assertSignedIn(resp.session, p.id)

        # sign out
        resp = resp.goto('/person/signout')

        print "resp.session", resp.session

        self.failIf('contact_id' in resp.session)
        
        # clean up
        self.dbsession.delete(self.dbsession.query(Person).get(p.id))
        self.dbsession.flush()

    def test_signin_invalid(self):
        """Test invalid login details"""
        # login
        resp = self.app.get(url_for(controller='/person', action='signin'))
        f = resp.form
        f['email_address'] = 'testguy'
        f['password'] = 'password'

        f.submit()

        self.failIf('contact_id' in resp.session)

    def test_signin_unconfirmed(self):
        # create an account
        p = model.core.Person(email_address='testguy@example.org',
                         password='p4ssw0rd',
			 handle='testguy')
        self.dbsession.save(p)
        self.dbsession.flush()
        pid = p.id
        
        # try to login
        resp = self.app.get(url_for(controller='person',
                                    action='signin'))
        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f['password'] = 'p4ssw0rd'
        resp = f.submit()
    
        # test that login is refused
        self.failIf('signed_in_person_id' in resp.session)
        
        # clean up
        self.dbsession.delete(self.dbsession.query(Person).get(p.id))
        self.dbsession.flush()

    def test_registration_confirmation(self):
        # insert registration model object
        timestamp = datetime.datetime.now()
        email_address = 'testguy@testguy.org'
        password = 'password'
	handle = 'testguy'
        r = Person(creation_timestamp=timestamp,
                   email_address=email_address,
                   password=password,
		   handle=handle,
                   activated=False)
        url_hash = r.url_hash
        print url_hash
        self.dbsession.save(r)
        self.dbsession.flush()
        rid = r.id
        print r
        # clear so that we reload the object later
        self.dbsession.clear()
        
        # visit the link
        response = self.app.get('/person/confirm/' + url_hash)
        response.mustcontain('Thanks for confirming your account')
        
        # test that it's activated
        r = self.dbsession.get(Person,rid)
        self.assertEqual(True, r.activated, "registration was not activated")

        # clean up
        self.dbsession.delete(self.dbsession.query(Person).get(rid))
        self.dbsession.flush()

    def test_registration_confirmation_invalid_url_hash(self):
        """test that an invalid has doesn't activate anything"""
        self.assertEmptyModel(Person)

        response = self.app.get('/person/confirm/nonexistent', status=404)

    def test_person_password_routing(self):
        self.assertEqual(dict(controller='person',
                              action='forgotten_password', id=None),
                         self.map.match('/person/forgotten_password'))

    def test_person_password_url_for(self):
        self.assertEqual('/person/forgotten_password',
                         url_for(controller='person', action='forgotten_password'))

    def test_person_confirm_routing(self):
        self.assertEqual(dict(controller='person',
                              action='reset_password',
                              url_hash='N'),
                         self.map.match('/person/reset_password/N'))

    def test_person_password_url_for(self):
        self.assertEqual('/person/reset_password/N',
                         url_for(controller='/person', action='reset_password', url_hash='N'))

    def test_forgotten_password(self):
        p = model.Person(email_address='testguy@example.org')
        self.dbsession.save(p)
        self.dbsession.flush()
        pid = p.id

        # trap smtp
        Dummy_smtplib.install()

        # get the login page
        resp = self.app.get(url_for(controller='person',
            action='signin', id=None))
        # click on the forgotten password link
        resp = resp.click('Forgotten your password?')

        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f.submit()

        # check that the confirmation record was created
        crecs = self.dbsession.query(PasswordResetConfirmation).filter_by(email_address='testguy@example.org').all()
        self.failIfEqual(0, len(crecs))

        # check our email
        self.failIfEqual(None, Dummy_smtplib.existing, "no message sent from forgotten password action")

        print Dummy_smtplib.existing.message

        # check to address
        to_match = re.match(r'^.*To:.*testguy@example.org', Dummy_smtplib.existing.message, re.DOTALL)
        self.failIfEqual(None, to_match, "to address not in headers")

        # check that the email has no HTML in it and thus was not rendered
        # incorrectly
        html_match = re.match(r'^.*<!DOCTYPE', Dummy_smtplib.existing.message, re.DOTALL)
        self.assertEqual(None, html_match, "HTML in message")

        # check that the message has a url hash in it
        url_match = re.match(r'^.*(/person/reset_password/\S+)', Dummy_smtplib.existing.message, re.DOTALL)
        self.failIfEqual(None, url_match, "reset password url not found in message")

        # ok go to the URL, on treadmills
        resp = self.app.get(url_match.group(1))

        # set password
        f = resp.form
        f['password'] = 'passwdtest'
        f['password_confirm'] = 'passwdtest'
        f.submit()

        self.dbsession.clear()
        # check that the password was changed
        p_hash = md5.new('passwdtest').hexdigest()
        p = self.dbsession.get(Person, pid)
        self.assertEqual(p_hash, p.password_hash)

        # check that the confirmatin record is gone
        crecs = self.dbsession.query(PasswordResetConfirmation).filter_by(email_address='testguy@example.org').all()
        self.assertEqual(0, len(crecs))

        # clean up
        Dummy_smtplib.existing.reset()
        self.dbsession.delete(p)
        self.dbsession.flush()

    def test_forgotten_password_no_person(self):
        """Test that an invalid email address doesn't start a password change.
        """
        Dummy_smtplib.install()

        resp = self.app.get(url_for(controller='person',
                                    action='signin'))
        resp = resp.click('Forgotten your password?')
        f = resp.forms[0]
        f['email_address'] = 'nonexistent@example.org'
        resp = f.submit()

        #print resp
        resp.mustcontain("Your supplied e-mail does not exist in our database")

        crecs = self.dbsession.query(PasswordResetConfirmation).filter_by(email_address='nonexistent@example.org').all()
        self.assertEqual(0, len(crecs), "contact records found: %r" % crecs)
        self.assertEqual(None, Dummy_smtplib.existing)

    def test_confirm_404(self):
        """Test that an attempt to access an invalid url_hash throws a 404"""
        resp = self.app.get(url_for(action='reset_password',
            controller='person',
            url_hash='n'), status=404)

    def test_confirm_old_url_hash(self):
        """Test that old url_hashes are caught"""
        email = 'testguy@example.org'
        stamp = datetime.datetime.now() - datetime.timedelta(24, 0, 1)
        c = PasswordResetConfirmation(email_address=email)
        c.timestamp = stamp
        self.dbsession.save(c)
        self.dbsession.flush()
        cid = c.id

        resp = self.app.get(url_for(controller='person',
            action='reset_password',
            url_hash=c.url_hash))
        # check for warning
        resp.mustcontain("This password recovery session has expired")

        self.dbsession.clear()
        c = self.dbsession.get(PasswordResetConfirmation, cid)
        # record shouldn't exist anymore
        self.assertEqual(None, c)


    def test_confirm(self):
        """Test confirmation of a password reset that should succeed"""

        # create a confirmation record
        email = 'testguy@example.org'
        p = Person(email_address=email)
        self.dbsession.save(p)
        c = PasswordResetConfirmation(email_address=email)
        # set the timestamp to just under 24 hours ago
        c.timestamp = datetime.datetime.now() - datetime.timedelta(23, 59, 59)
        self.dbsession.save(c)
        self.dbsession.flush()
        pid = p.id
        cid = c.id

        resp = self.app.get(url_for(controller='person',
            action='reset_password',
            url_hash=c.url_hash))

        # showing the email on the page
        resp.mustcontain(email)

        f = resp.form
        f['password'] = 'test'
        f['password_confirm'] = 'test'
        resp = f.submit()

        # check for success
        resp.mustcontain("Your password has been updated")

        self.dbsession.clear()

        # conf rec should be gone
        c = self.dbsession.get(PasswordResetConfirmation, cid)
        self.assertEqual(None, c)

        # password should be set to 'test'
        p_hash = md5.new('test').hexdigest()
        p = self.dbsession.get(Person, pid)
        self.assertEqual(p_hash, p.password_hash)

        self.dbsession.delete(p)
        self.dbsession.flush()

    def test_duplicate_password_reset(self):
        """Try to reset a password twice.
        """
        c = Person(email_address='testguy@example.org')
        self.dbsession.save(c)
        self.dbsession.flush()
        cid = c.id

        #
        email = 'testguy@example.org'

        # trap smtp
        Dummy_smtplib.install()

        resp = self.app.get(url_for(controller='person',
                                    action='signin'))
        resp = resp.click('Forgotten your password?')
        f = resp.forms[0]
        f['email_address'] = email
        f.submit()

        crec = self.dbsession.query(PasswordResetConfirmation).filter_by(email_address=email).one()
        self.failIfEqual(None, crec)
        crecid = crec.id

        # submit a second time
        resp = f.submit()

        resp.mustcontain("password recovery process is already in progress")

        # clean up
        Dummy_smtplib.existing.reset()
        self.dbsession.delete(self.dbsession.query(PasswordResetConfirmation).get(crecid))
        self.dbsession.delete(self.dbsession.query(Person).get(cid))
        self.dbsession.flush()

    def test_login_failed_warning(self):
        """Test that you get an appropriate warning message from the form when you try to log in with invalid credentials.
        """
        resp = self.app.get(url_for(controller='person',
                                    action='signin', id=None))
        f = resp.form
        f['email_address'] = 'test'
        f['password'] = 'broken'
        resp = f.submit()

        resp.mustcontain("Your sign-in details are incorrect")


    def test_create_person(self):
        """Test the process of creating new persons.
        """
        Dummy_smtplib.install()
        
        # get the home page
        resp = self.app.get('/person/signin')
        # click on the 'create new account' link
        resp = resp.click('Sign up')
        # fill out the form
        f = resp.form
        f['person.email_address'] = 'testguy@example.org'
        f['person.firstname'] = 'Testguy'
        f['person.lastname'] = 'McTest'
        f['person.password'] = 'test'
        f['person.password_confirm'] = 'test'
        f['person.phone'] = '123'
        f['person.mobile'] = '123'
        f['person.address1'] = 'here'
        f['person.city'] = 'there'
        f['person.postcode'] = '1234'
        f['person.country'] = 'Australia'
        resp = f.submit()
        # did we get an appropriate page?
        resp.mustcontain("follow the instructions in that message")

        # check our email
        self.failIfEqual(None, Dummy_smtplib.existing,
                         "no message sent")
        message = Dummy_smtplib.existing
        # check that it went to the right place
        self.assertEqual("testguy@example.org", message.to_addresses)
        # check that the message has the to address in it
        to_match = re.match(r'^.*To:.*testguy@example.org.*',
                            message.message, re.DOTALL)
        self.failIfEqual(None, to_match, "to address not in headers")
        # check that the message has the user's name
        name_match = re.match(r'^.*Testguy.*McTest',
                              message.message, re.DOTALL)
        self.failIfEqual(None, name_match, "user's name not in headers")
        # check that the message was renderered without HTML, i.e.
        # as a fragment and thus no autohandler crap
        html_match = re.match(r'^.*<!DOCTYPE', message.message, re.DOTALL)
        self.failUnlessEqual(None, html_match, "HTML in message!")
        # check that the message has a url hash in it
        match = re.match(r'^.*/person/confirm/(\S+)',
                         message.message, re.DOTALL)
        self.failIfEqual(None, match, "url not found")
        # visit the url
        print "match: '''%s'''" % match.group(1)
        resp = self.app.get('/person/confirm/%s' % match.group(1))
        #print resp
        
        # check the rego worked
        regs = self.dbsession.query(Person).all()
        self.failIfEqual([], regs)
        #print regs[0]
        self.assertEqual(True, regs[0].activated, "account was not activated!")
        rid = regs[0].id
        # ok, now try to log in

        resp = resp.click('sign in')
        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f['password'] = 'test'
        resp = f.submit()
        self.failIf('details are incorrect' in resp)
        self.assertSignedIn(resp.session, rid)

        # clean up
        Dummy_smtplib.existing.reset()

        self.dbsession.delete(self.dbsession.query(Person).get(rid))
        self.dbsession.flush()

    def test_create_duplicate_person(self):
        Dummy_smtplib.install()
        
        # create a fake user
        p = Person(email_address='testguy@example.org')
        p.activated = True
        self.dbsession.save(p)
        self.dbsession.flush()
        pid = p.id

        resp = self.app.get('/person/new')
        f = resp.form
        f['person.email_address'] = 'testguy@example.org'
        f['person.firstname'] = 'Testguy'
        f['person.lastname'] = 'McTest'
        f['person.password'] = 'test'
        f['person.password_confirm'] = 'test'
        f['person.phone'] = '1234'
        f['person.mobile'] = '1234'
        f['person.address1'] = 'Moo St'
        f['person.city'] = 'Tassie'
        f['person.country'] = 'Australia'
        f['person.postcode'] = '2000'
        resp = f.submit()

        resp.mustcontain('A person with this email already exists.')

        resp.click('recover your password')

        self.dbsession.delete(self.dbsession.query(Person).get(pid))
        self.dbsession.flush()
