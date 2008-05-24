import md5

from sqlalchemy.orm import create_session

from zookeepr.lib.base import *
from zookeepr.model import Person, Role

class retcode:
    """Enumerations of authentication return codes"""
    # daily wtf eat your heart out
    SUCCESS = True
    FAILURE = False
    TRY_AGAIN = 3
    INACTIVE = 4

class PersonAuthenticator(object):
    """Look up the Person in the data store"""

    def authenticate(self, username, password):
        dbsession = create_session()

        person = dbsession.query(Person).filter_by(email_address=username).one()
        
        if person is None:
            return retcode.FAILURE

        password_hash = md5.new(password).hexdigest()

        if not person.activated:
            result = retcode.INACTIVE
        elif password_hash == person.password_hash:
            result = retcode.SUCCESS
        else:
            result = retcode.FAILURE

        dbsession.close()

        return result


# class AuthenticateValidator(formencode.FancyValidator):
#     def _to_python(self, value, state):
#         if state.authenticate(value['email_address'], value['password']):
#             return value
#         else:
#             raise formencode.Invalid('Incorrect password', value, state)

# class ExistingEmailAddress(formencode.FancyValidator):
#     def _to_python(self, value, state):
#         auth = state.auth
#         if not value:
#             raise formencode.Invalid('Please enter a value',
#                                      value, state)
#         elif not auth.user_exists(value):
#             raise formencode.Invalid('No such user', value, state)
#         return value
    
# class SignIn(formencode.Schema):
#     go = formencode.validators.String()
#     email_address = ExistingEmailAddress()
#     password = formencode.validators.String(not_empty=True)
#     chained_validators = [
#         AuthenticateValidator()
#         ]

# class UserModelAuthStore(object):
#     def __init__(self):
#         self.status = {}
        
#     def user_exists(self, value):
#         session = create_session()
#         ps = session.query(Person).select_by(email_address=value)
#         result = len(ps) > 0
#         return result

#     def sign_in(self, username):
#         self.status[username] = ()

#     def sign_out(self, username):
#         if self.status.has_key(username):
#             del self.status[username]

#     def authorise(self, email_address, role=None, signed_in=None):
#         if signed_in is not None:
#             is_signed_in = False
#             if self.status.has_key(email_address):
#                 is_signed_in = True

#             return signed_in and is_signed_in
        
#         return True

class SecureController(BaseController):
    """Restrict controller access to people who are logged in.

    Controllers that require someone to be logged in can inherit
    from this class instead of `BaseController`.
    
    In the permissions list, the special name 'ALL' sets the default
    (normally no access).

    Normally, users will be redirected to log in if they aren't already.
    If the permissions list for the action is just True, the action is
    permitted without login ("anonymous action").

    Example:
      permissions = { 'view': [AuthRole('reviewer'), AuthRole('organiser')],
                      'submit': True,
                      'ALL': [AuthRole('organiser)] }

    As a bonus, they will have access to `c.person` which is a
    `model.Person` object that will identify the user who is currently
    logged in. Anonymous actions then may or may not have a c.person.

    """

    def logged_in(self):
        # check that the user is logged in.
        # We can tell if someone is logged in by the presence
        # of the 'signed_in_person_id' field in the browser session.
        return 'signed_in_person_id' in session

    def __before__(self, **kwargs):
        # Call the parent __before__ method to ensure the common pre-call code
        # is run
        if hasattr(super(SecureController, self), '__before__'):
            super(SecureController, self).__before__(**kwargs)

        if self.logged_in():
            # Retrieve the Person object from the object store
            # and attach it to the magic 'c' global.
            c.signed_in_person = self.dbsession.query(Person).filter_by(id=session['signed_in_person_id']).one()

            # Setup some roles for mghty to utilise
            roles = self.dbsession.query(Role).all()
            for role in roles:
                r = AuthRole(role.name)
                if r.authorise(self):
                    setattr(c, 'is_%s_role' % role.name, True)


        elif not hasattr(self, 'permissions'):
            abort(403, "no permissions configured controller... denied")
        elif not self.permissions.has_key(kwargs['action']):
            abort(403, "no permissions configured for action... denied")
        elif self.permissions[kwargs['action']]==True:
            # No-one's logged in, but this action is OK with that.
            return
        else:
            # No-one's logged in, so send them to the signin page.

            # If we were being nice and WSGIy, we'd raise a 403 or 401 error
            # (depending) and let a security middleware layer take care
            # of the redirect.  Save that for a rainy day...
            session['sign_in_redirect'] = h.current_url()
            session.save()
            redirect_to(controller='person',
                        action='signin',
                        id=None)

        if self.check_permissions(kwargs['action']):
            return
        else:
            abort(403, "computer says no")

    def check_permissions(self, action):
        if not hasattr(self, 'permissions'):
             # no access by default
            return False

        if action in self.permissions.keys():
	    perms = self.permissions[action]
        elif 'ALL' in self.permissions.keys():
	    perms = self.permissions['ALL']
	else:
            # no access by default
	    return False

        if perms==True:
            # anonymous action
            return True

        results = map(lambda x: x.authorise(self), perms)
        return reduce(lambda x, y: x or y, results, False)

class AuthFunc(object):
    def __init__(self, callable):
        self.callable = callable

    def authorise(self, cls):
        result = getattr(cls, self.callable)()
        if result is None:
            # None is bad.  Return True or False
            raise RuntimeError, "AuthFunc didn't get a result from %r!  Make sure you return a boolean!" % self.callable
        return result

class AuthTrue(object):
    def authorise(self, cls):
        return True

class AuthFalse(object):
    def authorise(self, cls):
        return False

class AuthRole(object):
    def __init__(self, role_name):
        self.role_name = role_name

    def authorise(self, cls):
        role = cls.dbsession.query(Role).filter_by(name=self.role_name).first()
        retval = role in c.signed_in_person.roles
        return retval
