from zookeepr.lib.base import *

class RegisterController(BaseController):
    def index(self):
        #m.send_redirect(h.url_for('register', action='new'))
        errors, defaults = {}, m.request_args
        if defaults:
            form_result, errors = model.UserInfoSchema().validate(defaults)
            if not errors:
                model.UserInfo(**form_result) # database insert
                m.write("huzzah you are called %s and you registered lol" % form_result['username'])
                return m.subexec('thankyou.myt')
        m.subexec('register.myt', defaults=defaults, errors=errors)

    def remove(self, id):
        m.write("you're removing registration %s" % id)

    def edit(self, id):
        m.write("you're editing registration %s" % id)

    def view(self, id):
        m.write("you're viewing registratoin %s" % id)
