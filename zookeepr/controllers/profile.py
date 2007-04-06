from zookeepr.lib.base import *
from zookeepr.lib.crud import Read, Update, List
from zookeepr.lib.auth import AuthRole
from zookeepr import model
from zookeepr.model.core.domain import Role

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

    def view(self):
        # hack because we don't use SecureController
        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.get(model.Person, session['signed_in_person_id'])
            roles = self.dbsession.query(Role).select()
            for role in roles:
                r = AuthRole(role.name)
                if r.authorise(self):
                    setattr(c, 'is_%s_role' % role.name, True)


        return super(ProfileController, self).view()
