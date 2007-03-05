from zookeepr.lib.auth import SecureController, AuthFunc
from zookeepr.lib.base import *
from zookeepr.lib.crud import Read, Update
from zookeepr import model

class ProfileController(SecureController, Read, Update):
    model = model.Person
    individual = 'profile'

    permissions = {'view': [AuthFunc('is_same_id')]}

    def index(self):
        if not 'signed_in_person_id' in session:
            abort(403)

        redirect_to(action='view', id=session['signed_in_person_id'])

    def is_same_id(self, *args):
        return self.obj.id == session['signed_in_person_id']

