from formencode import validators, compound, variabledecode, ForEach
from formencode.schema import Schema

from zookeepr.lib.auth import *
from zookeepr.lib.base import *
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import *
from zookeepr.model import Person, Volunteer

class VolunteerSchema(BaseSchema):
    areas = DictSet()
    other = validators.String()

class NewVolunteerSchema(BaseSchema):
    volunteer = VolunteerSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditVolunteerSchema(BaseSchema):
    volunteer = VolunteerSchema()
    pre_validators = [variabledecode.NestedVariables]

class VolunteerController(SecureController, View, Modify):
    schemas = {"new" : NewVolunteerSchema(),
               "edit" : EditVolunteerSchema()}
    permissions = {"view": [AuthRole('organiser'), AuthFunc('is_same_person')],
                   "index": [AuthTrue()],
                   "edit": [AuthRole('organiser'), AuthFunc('is_same_person')],
                   "new": [AuthTrue()],
                   "accept": [AuthRole('organiser')],
                   "reject": [AuthRole('organiser')],
                   }

    model = Volunteer
    individual = 'volunteer'

    def is_same_person(self):
        return c.signed_in_person == c.volunteer.person

    def index(self):
        # Check access and redirect
        if not AuthRole('organiser').authorise(self):
            redirect_to(action='new')

        # This method is mostly implemented by crud
        if hasattr(super(VolunteerController, self), 'index'):
            return super(VolunteerController, self).index()

    def new(self):
        # A person can only volunteer once
        if c.signed_in_person and c.signed_in_person.volunteer:
            return redirect_to(action='edit', id=c.signed_in_person.volunteer.id)

        # This method is mostly implemented by crud
        if hasattr(super(VolunteerController, self), 'new'):
            return super(VolunteerController, self).new()

    def _new_presave(self):
        self.obj.person = c.signed_in_person

    def accept(self, id):
        self.obj.accepted = True
        self.dbsession.update(self.obj)
        self.dbsession.flush()
        redirect_to(action='index')

    def reject(self, id):
        self.obj.accepted = False
        self.dbsession.update(self.obj)
        self.dbsession.flush()
        redirect_to(action='index')
