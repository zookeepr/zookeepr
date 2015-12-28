from datetime import datetime, timedelta
import re

from zk.model import Person, PasswordResetConfirmation
from routes import url_for

from .fixtures import PersonFactory, PasswordResetConfirmationFactory
from .utils import do_login, isSignedIn

class TestPersonController(object):
    def test_registration_confirmation_url(self, map):
        """test the routing of the registration confirmation url"""
        expect = dict(controller='person', action='confirm', confirm_hash='N')
        assert map.match('/person/confirm/N') == expect

    def test_registratrion_confirmation_named_route(self):
        reg_confirm = url_for('acct_confirm', confirm_hash='N')
        assert reg_confirm == '/person/confirm/N'

    def test_person_signin_routing(self, map):
        expect = dict(controller='person', action='signin')
        assert map.match('/person/signin') == expect
        
    def test_person_signin_url(self):
        assert url_for(controller='person', action='signin', id=None) == '/person/signin'

    def test_person_signout_url(self):
        assert url_for(controller='person', action='signout', id=None) == '/person/signout'

    def test_signin_signout(self, app, db_session):
        """Test person sign in"""

        # create a user
        p = PersonFactory()
        db_session.commit()
        
        resp = do_login(app, p)
        assert isSignedIn(app)

        # see if we're still logged in when we go to another page
        resp = app.get(url_for(controller='home'))
        assert isSignedIn(app)

        # sign out
        resp = resp.goto('/person/signout')
        assert not isSignedIn(app)
        
    def test_signin_invalid(self, app, db_session):
        """Test invalid login details"""

        do_login(app, 'invalid-email', 'invalid-password')
        assert not isSignedIn(app)

    def test_signin_unconfirmed(self, app, db_session):
        # create a user
        p = PersonFactory(activated=False)
        db_session.commit()

        # Without activation you can log in but not register or put in a proposal
        resp = do_login(app, p)
        assert isSignedIn(app)
        resp.follow()

        resp = app.get('/programme/submit_a_proposal')
        resp = resp.follow()
        assert 'Check your email for activation instructions.' in unicode(resp.body, 'utf-8')

        resp = app.get('/register/status')
        resp = resp.follow()
        assert 'Check your email for activation instructions.' in unicode(resp.body, 'utf-8')

        resp = app.get('/registration/new')
        resp = resp.follow()
        assert 'Check your email for activation instructions.' in unicode(resp.body, 'utf-8')

    def test_registration_confirmation(self, app, db_session):
        # insert registration model object
        p = PersonFactory(activated=False)
        db_session.commit()

        # visit the link
        resp = app.get('/person/confirm/' + p.url_hash)
        assert 'Thanks for confirming your account' in unicode(resp.body, 'utf-8')

        # Need to forget the objects we created
        db_session.expunge_all()
        
        # test that it's activated
        r = Person.find_by_id(p.id)
        assert r.activated == True

    def test_registration_confirmation_invalid_url_hash(self, app, db_session):
        """test that an invalid has doesn't activate anything"""
        response = app.get('/person/confirm/nonexistent', status=404)
        assert response.status_code == 404

    def test_person_password_routing(self, map):
        expect = dict(controller='person', action='forgotten_password')
        assert map.match('/person/forgotten_password') == expect

    def test_person_password_url_for(self):
        assert url_for(controller='person', action='forgotten_password') == '/person/forgotten_password'

    def test_person_confirm_routing(self, map):
        expect = dict(controller='person', action='reset_password', url_hash='N')
        assert map.match('/person/reset_password/N') == expect

    def test_person_password_url_for(self):
        assert url_for(controller='/person', action='reset_password', url_hash='N') == '/person/reset_password/N'

    def test_forgotten_password_full_process(self, app, db_session, smtplib):
        p = PersonFactory(activated=False)
        db_session.commit()

        # get the login page
        resp = app.get(url_for(controller='person', action='signin', id=None))
        # click on the forgotten password link
        resp = resp.click('Forgotten your password?')

        f = resp.forms['pwreset-form']
        f['email_address'] = p.email_address
        f.submit()

        # check that the confirmation record was created
        crecs = PasswordResetConfirmation.find_by_email(p.email_address)
        assert crecs is not None

        # check our email
        assert smtplib.existing != None

        # check to address
        to_match = re.match(r'^.*To:.*' + p.email_address, smtplib.existing.message, re.DOTALL)
        assert to_match != None

        # check that the email has no HTML in it and thus was not rendered
        # incorrectly
        html_match = re.match(r'^.*<!DOCTYPE', smtplib.existing.message, re.DOTALL)
        assert html_match == None

        # check that the message has a url hash in it
        url_match = re.match(r'^.*(/person/reset_password/\S+)', smtplib.existing.message, re.DOTALL)
        assert url_match != None

        # ok go to the URL, on treadmills
        resp = app.get(url_match.group(1))

        # set password
        f = resp.forms['reset-form']
        f['password'] = 'passwdtest'
        f['password_confirm'] = 'passwdtest'
        resp = f.submit(extra_environ=dict(REMOTE_ADDR='0.0.0.0'))

        # Need to forget the objects we created, save ones that need saving
        pid = p.id
        old_hash = p.password_hash
        db_session.expunge_all()

        # check that the password was changed
        p = Person.find_by_id(pid)
        assert p.password_hash != old_hash

        # check that the confirmatin record is gone
        crecs = PasswordResetConfirmation.find_by_email(p.email_address)
        assert crecs is None

    def test_forgotten_password_no_person(self, app, db_session, smtplib):
        """Test that an invalid email address doesn't start a password change.  """

        resp = app.get(url_for(controller='person', action='signin'))
        resp = resp.click('Forgotten your password?')
        f = resp.forms['pwreset-form']
        f['email_address'] = 'nonexistent@example.org'
        resp = f.submit()

        # Old behaviour was to report that the address didn't exist
        # This is a mild security leak and was changed at some point
        # Change discussed and confirmed in #413
        # New behaviour is to display the standard prompt page
        # An email is also sent to the given address indicating the attempt

        # Standard response page
        assert "complete the password reset process" in unicode(resp.body, 'utf-8')

        # No reset entry created, no find_all method
        assert db_session.query(PasswordResetConfirmation).count() == 0

        # Email sent
        assert "nonexistent@example.org" in smtplib.existing.to_addresses

    def test_confirm_404(self, app):
        """Test that an attempt to access an invalid url_hash throws a 404"""
        resp = app.get(url_for(action='reset_password',
                               controller='person',
                               url_hash='n'
                              ),
                       status=404
                      )

    def test_confirm_old_url_hash(self, app, db_session):
        """Test that old url_hashes are caught"""

        stamp = datetime.now() - timedelta(days=1.1)
        c = PasswordResetConfirmationFactory(timestamp = stamp)
        db_session.commit()

        resp = app.get(url_for(controller='person',
            action='reset_password',
            url_hash=c.url_hash))

        # TODO: Ensure confirm must match

        # Prompted to enter new password
        f = resp.forms['reset-form']
        f['password'] = 'test'
        f['password_confirm'] = 'test'
        resp =  f.submit(extra_environ=dict(REMOTE_ADDR='0.0.0.0'))

        # check for warning
        assert "This password recovery session has expired" in unicode(resp.body, 'utf-8')

        # Need to forget the objects we created
        db_session.expunge_all()

        # Outstanding confirmation should be gone
        crecs = PasswordResetConfirmation.find_by_email(c.email_address)
        assert crecs is None


    def test_confirm_reset(self, app, db_session):
        """Test confirmation of a password reset that should succeed"""

        # create a confirmation record
        p = PersonFactory()
        # set the timestamp to just under 24 hours ago
        stamp = datetime.now() - timedelta(days=0.9)
        c = PasswordResetConfirmationFactory(email_address=p.email_address, timestamp=stamp)
        db_session.commit()

        resp = app.get(url_for(controller='person',
            action='reset_password',
            url_hash=c.url_hash))

        # showing the email on the page
        assert c.email_address in unicode(resp.body, 'utf-8')

        f = resp.forms['reset-form']
        f['password'] = 'test'
        f['password_confirm'] = 'test'
        resp =  f.submit(extra_environ=dict(REMOTE_ADDR='0.0.0.0'))
        resp = resp.maybe_follow()

        # check for success
        assert "Your password has been updated" in unicode(resp.body, 'utf-8')

        # Need to forget the objects we created, save portions we need
        pid = p.id
        old_password_hash = p.password_hash
        db_session.expunge_all()

        # conf rec should be gone
        crecs = PasswordResetConfirmation.find_by_email(c.email_address)
        assert crecs is None

        # password should be changed
        p = Person.find_by_id(pid)
        assert p.password_hash == old_password_hash

    def test_duplicate_password_reset(self, app, db_session, smtplib):
        """Try to reset a password twice.  """

        p = PersonFactory()
        db_session.commit()

        resp = app.get(url_for(controller='person', action='signin'))
        resp = resp.click('Forgotten your password?')
        f = resp.forms['pwreset-form']
        f['email_address'] = p.email_address
        f.submit()

        crec = PasswordResetConfirmation.find_by_email(p.email_address)
        assert crec is not None

        # submit a second time
        resp = f.submit()
        assert "password recovery process is already in progress" in unicode(resp.body, 'utf-8')

    def test_login_failed_warning(self, app, db_session):
        """Test that you get an appropriate warning message from the form when you try to log in with invalid credentials.
        """

        resp = app.get(url_for(controller='person', action='signin', id=None))
        f = resp.forms['signin-form']
        f['person.email_address'] = 'test@failure.zk'
        f['person.password'] = 'broken'
        resp = f.submit()

        assert "Your sign-in details are incorrect" in unicode(resp.body, 'utf-8')


    def test_create_person(self, app, db_session, smtplib):
        """Test the process of creating new persons.  """

        # get the home page
        resp = app.get('/person/signin')
        # click on the 'create new account' link
        resp = resp.click('Sign up')
        # fill out the form
        f = resp.form
        f['person.email_address']    = 'testguy@example.org'
        f['person.firstname']        = 'Testguy'
        f['person.lastname']         = 'McTest'
        f['person.password']         = 'test'
        f['person.password_confirm'] = 'test'
        f['person.phone']            = '123'
        f['person.mobile']           = '123'
        f['person.address1']         = 'here'
        f['person.city']             = 'there'
        f['person.postcode']         = '1234'
        f['person.country']          = 'AUSTRALIA'
        f['person.i_agree']          = '1'
        resp = f.submit(extra_environ=dict(REMOTE_ADDR='0.0.0.0'))

        # did we get an appropriate page?
        resp = resp.maybe_follow() # Shake out redirects
        assert "Check your email" in unicode(resp.body, 'utf-8')

        # check our email
        assert smtplib.existing is not None
        message = smtplib.existing

        # check that it went to the right place
        assert "testguy@example.org" in message.to_addresses

        # check that the message has the to address in it
        to_match = re.match(r'^.*To:.*testguy@example.org.*', message.message, re.DOTALL)
        assert to_match is not None

        # check that the message has the user's name
        name_match = re.match(r'^.*Testguy.*McTest', message.message, re.DOTALL)
        assert name_match is not None

        # check that the message was renderered without HTML, i.e.
        # as a fragment and thus no autohandler crap
        html_match = re.match(r'^.*<!DOCTYPE', message.message, re.DOTALL)
        assert html_match is None

        # check that the message has a url hash in it
        match = re.match(r'^.*/person/confirm/(\S+)', message.message, re.DOTALL)
        assert match is not None

        # visit the url
        resp = app.get('/person/confirm/%s' % match.group(1))
        
        # check the rego worked
        reg = Person.find_by_email('testguy@example.org')
        assert reg is not None
        assert reg.activated == True

        # We should be automatically signed in
        assert isSignedIn(app)

        # Log out, so we can log in again
        resp = resp.goto('/person/signout')
        resp = resp.maybe_follow()
        assert not isSignedIn(app)

        # Ensure login works
        resp = resp.click('Sign in')
        f = resp.forms['signin-form']
        f['person.email_address'] = 'testguy@example.org'
        f['person.password'] = 'test'
        resp = f.submit(extra_environ=dict(REMOTE_ADDR='0.0.0.0'))
        assert 'details are incorrect' not in resp
        assert isSignedIn(app)

    # TODO: Test Config.get('account_creation') == false

    def test_create_duplicate_person(self, app, db_session):
        
        # create a fake user
        p = PersonFactory()
        db_session.commit()

        resp = app.get('/person/new')
        print resp
        f = resp.form
        f['person.email_address']    = p.email_address
        f['person.firstname']        = 'Testguy'
        f['person.lastname']         = 'McTest'
        f['person.password']         = 'test'
        f['person.password_confirm'] = 'test'
        f['person.phone']            = '123'
        f['person.mobile']           = '123'
        f['person.address1']         = 'here'
        f['person.city']             = 'there'
        f['person.postcode']         = '1234'
        f['person.country']          = 'AUSTRALIA'
        f['person.i_agree']          = '1'
        resp = f.submit(extra_environ=dict(REMOTE_ADDR='0.0.0.0'))

        assert 'A person with this email already exists.' in unicode(resp.body, 'utf-8')
        
        resp.click('recover your password')
