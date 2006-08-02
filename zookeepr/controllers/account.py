import formencode

#from zookeepr.lib.auth import SecureController, SignIn
from zookeepr.lib.base import *

class AccountController(BaseController):

    def index(self, **params):
        #return self.signin(**params)
        pass

#     def signin(self, ARGS, **params):
#         if len(ARGS):
#             validator = SignIn()

#             try:
#                 #if not request.environ.has_key('paste.login.http_login'):
#                 #    raise Exception('Action permissions specified but security middleware not present.')
#                 state = State()
#                 state.auth = g.auth
#                 state.authenticate = request.environ['paste.login.authenticator']().check_auth
#                 results = validator.to_python(ARGS, state=state)
#             except formencode.Invalid, e:
#                 # Note error_dict doesn't contain strings
#                 errors = e.error_dict
#                 if not e.error_dict:
#                     errors = {'password':str(e)}
#                 self.c.form = formbuild.Form(defaults=ARGS, errors=errors)
#                 return render_response('/account/signin.myt')
#             else:
#                 self.__signin__(username=ARGS.get('email_address'))
#                 return render_response('/account/signedin.myt', **ARGS)
#         else:
#             self.c.form = formbuild.Form(defaults=ARGS)
#             return render_response('/account/signin.myt')

#     def signout(self, ARGS, **params):
#         if request.environ.has_key('REMOTE_USER'):
#             self.__signout__(request.environ['REMOTE_USER'])
#             return render_response('/account/signedout.myt', **ARGS)
#         else:
#             return render_response('/account/alreadyout.myt', **ARGS)
