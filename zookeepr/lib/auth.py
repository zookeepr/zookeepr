import md5

from authkit.middleware import Authenticator
from authkit.controllers import PylonsSecureController
import pylons
from sqlalchemy import create_session

from zookeepr.models import Person

class UserModelAuthenticator(Authenticator):
    """Look up the user in the database"""

    def check_auth(self, username, password):
        session = create_session()
        ps = session.query(Person).select_by(handle=username)
        if len(ps) <> 1:
            return False

        password_hash = md5.new(password).hexdigest()
        
        result = password_hash == ps[0].password_hash
        session.close()
        return result

class UserModelAuthStore(object):
    def __init__(self):
        self.status = {}
        
    def user_exists(self, value):
        session = create_session()
        ps = session.query(Person).select_by(handle=value)
        result = len(ps) > 0
        return result

    def sign_in(self, username):
        self.status[username] = ()

    def sign_out(self, username):
        if self.status.has_key(username):
            del self.status[username]

    def authorise(self, username, role=None, signed_in=None):
        if signed_in is not None:
            is_signed_in = False
            if self.status.has_key(username):
                is_signed_in = True

            return signed_in and is_signed_in
        
        return True

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
        g = pylons.request.environ['pylons.g']
        
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
