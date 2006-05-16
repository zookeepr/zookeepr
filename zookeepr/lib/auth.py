import md5

import pylons
from authkit.middleware import Authenticator
from authkit.controllers import PylonsSecureController

from zookeepr.models import Person

class UserModelAuthenticator(Authenticator):
    """Look up the user in the database"""

    def check_auth(self, username, password):
        ps = Person.select_by(handle=username)
        if len(ps) <> 1:
            return False

        password_hash = md5.new(password).hexdigest()
        return password_hash == ps[0].password_hash

class UserModelAuthStore(object):
    def user_exists(self, value):
        ps = Person.select_by(handle=value)
        return len(ps) > 0

    def sign_in(self, username):
        pass

    def sign_out(self, username):
        pass

class SecureController(PylonsSecureController):
    def __granted__(self, action):
        action_ = getattr(self, action)

        if hasattr(action_, 'permissions'):
            if not pylons.request.environ.has_key('paste.login.http_login'):
                raise Exception("action permissions specified but security middleware not present")
            if pylons.request.environ.has_key('REMOTE_USER'):
                if self.__authorize__(pylons.request.environ['REMOTE_USER'], action_.permissions):
                    return True
                else:
                    pylons.m.abort(403, 'Computer says no')
            else:
                pylons.m.abort(401, 'Not signed in')
        else:
            return True

    def __authorize__(self, signed_in_user, ps):
        permissions = {}
        g = request.environ['pylons.g']
        
        for k, v in ps.items():
            permissions[k] = v

        def valid():
            if permissions.has_key('username'):
                if signed_in_user.lower() <> permissions['username'].lower():
                    return False
            else:
                permissions['username'] = signed_in_user

            if not g.auth.user_exists(permissions['username']):
                return False
            else:
                return g.auth.authorise(**permissions)

        if valid():
            return True
        else:
            self.__signout__(permissions['username'])
            return False
