import md5

from sqlalchemy import create_session

from zookeepr.lib.base import BaseController, c, g, redirect_to, session, abort
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

        objectstore = create_session()
        
        ps = objectstore.query(Person).select_by(email_address=username)
        
        if len(ps) <> 1:
            return retcode.FAILURE

        password_hash = md5.new(password).hexdigest()

        if not ps[0].activated:
            result = retcode.INACTIVE
        elif password_hash == ps[0].password_hash:
            result = retcode.SUCCESS
        else:
            result = retcode.FAILURE

        objectstore.close()
        
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

    As a bonus, they will have access to `c.person` which is a
    `model.Person` object that will identify the user
    who is currently logged in.
    """

    def logged_in(self):
        # check that the user is logged in.
        # We can tell if someone is logged in by the presence
        # of the 'signed_in_person_id' field in the browser session.
        return 'signed_in_person_id' in session

    def __before__(self, **kwargs):
        # Call the parent __before__ method to ensure the common pre-call code
        # is run
        super(SecureController, self).__before__(**kwargs)

        if self.logged_in():
            # Retrieve the Person object from the object store
            # and attach it to the magic 'c' global.
            # FIXME get is boned on the live site
            #c.person = g.objectstore.get(Person, session['signed_in_person_id'])
            c.person = g.objectstore.query(Person).select_by(id=session['signed_in_person_id'])[0]
        else:
            # No-one's logged in, so send them to the signin
            # page.
            # If we were being nice and WSGIy, we'd raise a 403 or 401 error
            # (depending) and let a security middleware layer take care
            # of the redirect.  Save that for a rainy day...
            redirect_to(controller='account',
                        action='signin',
                        id=None)

        if self.check_permissions(kwargs['action']):
            return
        else:
            abort(403, "computer says no")

    def check_permissions(self, action):
        if not hasattr(self, 'permissions'):
             # Open access by default
            return True

        if not action in self.permissions.keys():
            # open access by default
            return True

        results = map(lambda x: x.authorise(self), self.permissions[action])
        return reduce(lambda x, y: x or y, results, False)

class AuthFunc(object):
    def __init__(self, callable):
        self.callable = callable

    def authorise(self, cls):
        return getattr(cls, self.callable)()

class AuthTrue(object):
    def authorise(self):
        return True

class AuthFalse(object):
    def authorise(self):
        return False

class AuthRole(object):
    def __init__(self, role_name):
        self.role_name = role_name

    def authorise(self, cls):
        #print g.objectstore.query(Role).select()
        roles = g.objectstore.query(Role).select_by(name=self.role_name)
        #print "roles:", roles
        if len(roles) == 0:
            role = None
        else:
            role = roles[0]
        return role in c.person.roles
