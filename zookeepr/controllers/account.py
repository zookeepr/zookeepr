import datetime
import smtplib

from formencode import validators, Invalid
from formencode.schema import Schema
from formencode.variabledecode import NestedVariables
import sqlalchemy

from zookeepr.lib.auth import PersonAuthenticator, retcode
from zookeepr.lib.base import *
from zookeepr.lib.validators import BaseSchema
from zookeepr.model import Person, PasswordResetConfirmation

class AuthenticationValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        l = PersonAuthenticator()
        r = l.authenticate(value['email_address'], value['password'])
        if r == retcode.SUCCESS:
            pass
        elif r == retcode.FAILURE:
            raise Invalid("Your sign-in details are incorrect.", value, state)
        elif r == retcode.TRY_AGAIN:
            raise Invalid("A problem occurred during sign in; please try again later.", value, state)
        elif r == retcode.INACTIVE:
            raise Invalid("You haven't yet confirmed your registration, please refer to your email for instructions on how to do so.", value, state)
        else:
            raise RuntimeError, "Unhandled authentication return code: '%r'" % r


class ExistingAccountValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        accounts = state.query(Person).select_by(email_address=value['email_address'])
        if len(accounts) == 0:
            raise Invalid("Your sign-in details are incorrect; try registering a new account.", value, state)


class LoginValidator(BaseSchema):
    email_address = validators.String(not_empty=True)
    password = validators.String(not_empty=True)

    chained_validators = [ExistingAccountValidator(), AuthenticationValidator()]


class ForgottenPasswordSchema(BaseSchema):
    email_address = validators.String(not_empty=True)

    chained_validators = [ExistingAccountValidator()]


class PasswordResetSchema(BaseSchema):
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)

    chained_validators = [validators.FieldsMatch('password', 'password_confirm')]


# FIXME: merge with registration controller validator and move to validators
class NotExistingAccountValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        account = state.query(Person).get_by(email_address=value['email_address'])
        if account is not None:
            raise Invalid("This account already exists.  Please try signing in first.", value, state)


# FIXME: merge with registration controller validator and move to validators
class NotExistingHandleValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        account = state.query(Person).get_by(handle=value['handle'])
        if account is not None:
            raise Invalid("This handle already exists.  Please try signing in first, or choosing a new handle.", value, state)


class PersonSchema(Schema):
    email_address = validators.String(not_empty=True)
    fullname = validators.String(not_empty=True)
    handle = validators.String(not_empty=True)
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)
    
    chained_validators = [NotExistingAccountValidator(), NotExistingHandleValidator(), validators.FieldsMatch('password', 'password_confirm')]


class NewRegistrationSchema(BaseSchema):
    registration = PersonSchema()

    pre_validators = [NestedVariables]


class AccountController(BaseController):

    def signin(self):
        defaults = dict(request.POST)
        errors = {}

        if defaults:
            result, errors = LoginValidator().validate(defaults, self.dbsession)

            if not errors:
                # do the authorisation here or in validator?
                # get account
                # check auth
                # set session cookies
                person = self.dbsession.query(Person).get_by(email_address=result['email_address'])
                if person:
                    # at least one Person matches, save it
                    session['signed_in_person_id'] = person.id
                    session.save()

                    # Redirect to original URL if it exists
                    if 'sign_in_redirect' in session:
                        redirect_to(session['sign_in_redirect'])

                    # return home
                    redirect_to('home')

        return render_response('account/signin.myt', defaults=defaults, errors=errors)

    def signout(self):
        # delete and invalidate the session
        session.delete()
        session.invalidate()
        # return home
        redirect_to('home')

    def confirm(self, id):
        """Confirm a registration with the given ID.

        `id` is a md5 hash of the email address of the registrant, the time
        they regsitered, and a nonce.

        """
        r = self.dbsession.query(Person).select_by(url_hash=id)

        if len(r) < 1:
            abort(404)

        r[0].activated = True

        self.dbsession.save(r[0])
        self.dbsession.flush()

        return render_response('account/confirmed.myt')

    def forgotten_password(self):
        """Action to let the user request a password change.

        GET returns a form for emailing them the password change
        confirmation.

        POST checks the form and then creates a confirmation record:
        date, email_address, and a url_hash that is a hash of a
        combination of date, email_address, and a random nonce.

        The email address must exist in the account database.

        The second half of the password change operation happens in
        the ``confirm`` action.
        """
        defaults = dict(request.POST)
        errors = {}

        if defaults:
            result, errors = ForgottenPasswordSchema().validate(defaults, self.dbsession)

            if not errors:
                c.conf_rec = PasswordResetConfirmation(result['email_address'])
                self.dbsession.save(c.conf_rec)
                try:
                    self.dbsession.flush()
                except sqlalchemy.exceptions.SQLError, e:
                    self.dbsession.clear()
                    # FIXME exposes sqlalchemy!
                    return render_response('account/in_progress.myt')

                s = smtplib.SMTP("localhost")
                # generate email from template
                body = render('account/confirmation_email.myt', fragment=True)
                s.sendmail("support@anchor.com.au",
                    c.conf_rec.email_address,
                    body)
                s.quit()
                return render_response('account/password_confirmation_sent.myt')
        return render_response('account/forgotten_password.myt', defaults=defaults, errors=errors)


    def reset_password(self, url_hash):
        """Confirm a password change request, and let the user change
        their password.

        `url_hash` is a hash of the email address, with which we can
        look up the confuirmation record in the database.

        If `url_hash` doesn't exist, 404.

        If `url_hash` exists and the date is older than 24 hours,
        warn the user, offer to send a new confirmation, and delete the
        confirmation record.

        GET returns a form for setting their password, with their email
        address already shown.

        POST checks that the email address (in the session, not in the
        form) is part of a valid account record (again).  If the record
        exists, then update the password, hashed.  Report success to the
        user.  Delete the confirmation record.

        If the record doesn't exist, throw an error, delete the
        confirmation record.
        """
        crecs = self.dbsession.query(PasswordResetConfirmation).select_by(url_hash=url_hash)
        if len(crecs) == 0:
            abort(404)

        c.conf_rec = crecs[0]

        now = datetime.datetime.now()
        delta = now - c.conf_rec.timestamp
        if delta > datetime.timedelta(24, 0, 0):
            # this confirmation record has expired
            self.dbsession.delete(c.conf_rec)
            self.dbsession.flush()
            return render_response('account/expired.myt')

        # now process the form
        defaults = dict(request.POST)
        errors = {}

        if defaults:
            result, errors = PasswordResetSchema().validate(defaults, self.dbsession)

            if not errors:
                accounts = self.dbsession.query(Person).select_by(email_address=c.conf_rec.email_address)
                if len(accounts) == 0:
                    raise RuntimeError, "Account doesn't exist %s" % c.conf_rec.email_address

                # set the password
                accounts[0].password = result['password']
                # also make sure the account is activated
                accounts[0].activated = True
                
                # delete the conf rec
                self.dbsession.delete(c.conf_rec)
                self.dbsession.flush()

                return render_response('account/success.myt')

        # FIXME: test the process above
        return render_response('account/reset.myt', defaults=defaults, errors=errors)


    def new(self):
        """Create a new account.

        Non-CFP accounts get created through this interface.

        See ``cfp.py`` for more account creation code.
        """
        defaults = dict(request.POST)
        errors = {}

        if defaults:
            result, errors = NewRegistrationSchema().validate(defaults, self.dbsession)

            if not errors:
                c.person = Person()
                # update the objects with the validated form data
                for k in result['registration']:
                    setattr(c.person, k, result['registration'][k])
                self.dbsession.save(c.person)
                self.dbsession.flush()

                s = smtplib.SMTP("localhost")
                # generate welcome message
                body = render('account/new_account_email.myt',
                              fragment=True)
                s.sendmail(request.environ['paste.config']['app_conf'].get('committee_email'),
                           c.person.email_address,
                           body)
                s.quit()
                return render_response('account/thankyou.myt')

        return render_response('account/new.myt',
                               defaults=defaults, errors=errors)
