import md5

from authkit.middleware import Authenticator

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
