from zookeepr.lib.base import *
from zookeepr.lib.crud import Read, Update
from zookeepr import model

class ProfileController(BaseController, Read, Update):
    model = model.Person
    individual = 'profile'

    def index(self):
        if not 'signed_in_person_id' in session:
            abort(403)

        redirect_to(action='view', id=session['signed_in_person_id'])
