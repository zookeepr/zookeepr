from formencode import validators, Invalid

from zookeepr.lib.auth import PersonAuthenticator, retcode
from zookeepr.lib.base import *
from zookeepr.lib.validators import BaseSchema
from zookeepr.model import Person

class AuthenticationValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        l = PersonAuthenticator()
        r = l.authenticate(value['email_address'], value['password'])
        if r == retcode.SUCCESS:
            pass
        elif r == retcode.FAILURE:
            raise Invalid("Incorrect email address or password.", value, state)
        elif r == retcode.TRY_AGAIN:
            raise Invalid("A problem occurred during sign in; please try again later.", value, state)
        elif r == retcode.INACTIVE:
            raise Invalid("You haven't yet confirmed your registration, please refer to your email for instructions on how to do so.", value, state)
        else:
            raise RuntimeError, "Unhandled authentication return code: '%r'" % r

class LoginValidator(BaseSchema):
    email_address = validators.String(not_empty=True)
    password = validators.String(not_empty=True)

    chained_validators = [AuthenticationValidator()]

class AccountController(BaseController):

    def signin(self):
        defaults = dict(request.POST)
        errors = {}

        if defaults:
            result, errors = LoginValidator().validate(defaults)

            if not errors:
                # do the authorisation here or in validator?
                # get account
                # check auth
                # set session cookies
                persons = g.objectstore.query(Person).select_by(email_address=result['email_address'])
                if len(persons) < 1:
                    # Don't raise an exception, handle gracefully
                    errors = {'x': 'Invalid login'}
                else:
                    # at least one Person matches, save it
                    session['person_id'] = persons[0].id
                    session.save()

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
        r = g.objectstore.query(Person).select_by(url_hash=id)

        if len(r) < 1:
            abort(404)

        r[0].activated = True

        g.objectstore.save(r[0])
        g.objectstore.flush()

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
