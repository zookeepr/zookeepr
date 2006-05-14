from authkit.controllers import *

from zookeepr.lib.base import *

class SecurityController(BaseController, PylonsSecureController):

    def index(self, **params):
        return self.signin(**params)

    def signin(self, ARGS, **params):
        if len(ARGS):
            from authkit.validators import SignIn
            validator = SignIn()
            try:
                if not request.environ.has_key('paste.login.http_login'):
                    raise Exception('Action permissions specified but security middleware not present.')
                state = State()
                state.auth = g.auth
                state.authenticate = request.environ['paste.login.authenticator']().check_auth
                results = validator.to_python(ARGS, state=state)
            except formencode.Invalid, e:
                # Note error_dict doesn't contain strings
                errors = e.error_dict
                if not e.error_dict:
                    errors = {'password':str(e)}
                self.c.form = formbuild.Form(defaults=ARGS, errors=errors)
                m.subexec('/security/signin.myt')
            else:
                self.__signin__(username=ARGS.get('username'))
                m.subexec('/security/signedin.myt', **ARGS)
        else:
            self.c.form = formbuild.Form(defaults=ARGS)
            m.subexec('/security/signin.myt')

    def signout(self, ARGS, **params):
        if request.environ.has_key('REMOTE_USER'):
            self.__signout__(request.environ['REMOTE_USER'])
            m.subexec('/security/signedout.myt', **ARGS)
        else:
            m.subexec('/security/alreadyout.myt', **ARGS)
