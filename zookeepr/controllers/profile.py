from zookeepr.lib.base import *
from zookeepr.lib.crud import Read, Update, List
from zookeepr.lib.auth import AuthRole
from zookeepr import model

class ProfileController(BaseController, Read, Update, List):
    model = model.Person
    individual = 'profile'

    def index(self):
        r = AuthRole('organiser')
        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.get(model.Person, session['signed_in_person_id'])
            if not r.authorise(self):
                redirect_to(action='view', id=session['signed_in_person_id'])
        else:
            abort(403)

        return super(ProfileController, self).index()

    def view(self, id):
        # Give template access to dbsession for auth checks
        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.get(model.Person, session['signed_in_person_id'])
            r = AuthRole('organiser')
            if r.authorise(self):
                c.allowed_full = True

        return super(ProfileController, self).view()
