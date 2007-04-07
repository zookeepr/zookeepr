from zookeepr.lib.base import *
from zookeepr.lib.crud import Read, Update, List
from zookeepr.lib.auth import SecureController, AuthRole, AuthFunc
from zookeepr import model
from zookeepr.model.core.domain import Role

class ProfileController(SecureController, Read, Update, List):
    model = model.Person
    individual = 'profile'

    permissions = {'view': [AuthFunc('is_same_id')]}

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

    def is_same_id(self, *args):
        return self.obj.id == session['signed_in_person_id']
