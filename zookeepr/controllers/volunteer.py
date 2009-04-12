import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, DictSet
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model.volunteer import Volunteer

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)

class VolunteerSchema(BaseSchema):
    areas = DictSet()
    # TODO: test with not_empty=True and have the error be reported
    # next to the field instead of at the top of the file
    other = validators.String()

class NewVolunteerSchema(BaseSchema):
    volunteer = VolunteerSchema()
    pre_validators = [NestedVariables]

class EditVolunteerSchema(BaseSchema):
    volunteer = VolunteerSchema()
    pre_validators = [NestedVariables]

class VolunteerController(BaseController):

    @dispatch_on(POST="_new") 
    @authorize(h.auth.is_valid_user)
    def new(self):
        # A person can only volunteer once
        if h.signed_in_person() and h.signed_in_person().volunteer:
            return redirect_to(action='edit', id=h.signed_in_person().volunteer.id)

        return render('/volunteer/new.mako')

    @validate(schema=NewVolunteerSchema(), form='new')
    def _new(self):
        results = self.form_result['volunteer']

        c.volunteer = Volunteer(**results)
        c.volunteer.person = h.signed_in_person()
        meta.Session.add(c.volunteer)
        meta.Session.commit()

        h.flash("Volunteer application submitted. Thank you for your interest.")
        redirect_to(action='view', id=c.volunteer.id)

    @authorize(h.auth.is_valid_user)
    def view(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.can_edit = h.auth.is_same_zookeepr_user(id)

        c.volunteer = Volunteer.find_by_id(id)
        if c.volunteer is None:
            abort(404, "No such object")

        return render('volunteer/view.mako')

    def index(self):
        # Check access and redirect
        if not h.auth.has_organiser_role:
            redirect_to(action='new')

        c.volunteer_collection = Volunteer.find_all()
        return render('volunteer/list.mako')

    @dispatch_on(POST="_edit") 
    @authorize(h.auth.is_valid_user)
    def edit(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.volunteer = Volunteer.find_by_id(id)
        if c.volunteer.accepted is not None:
            return render('volunteer/already.mako')

        defaults = h.object_to_defaults(c.volunteer, 'volunteer')

        form = render('volunteer/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditVolunteerSchema(), form='edit')
    def _edit(self, id):
        volunteer = Volunteer.find_by_id(id)

        for key in self.form_result['volunteer']:
            setattr(volunteer, key, self.form_result['volunteer'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("Your details were updated successfully.")
        redirect_to(action='view', id=id)

    @authorize(h.auth.has_organiser_role)
    def accept(self, id):
        volunteer = Volunteer.find_by_id(id)
        volunteer.accepted = True
        meta.Session.commit()
        h.flash('Status Updated')
        redirect_to(action='index')

    @authorize(h.auth.has_organiser_role)
    def pending(self, id):
        volunteer = Volunteer.find_by_id(id)
        volunteer.accepted = None
        meta.Session.commit()
        h.flash('Status Updated')
        redirect_to(action='index')

    @authorize(h.auth.has_organiser_role)
    def reject(self, id):
        volunteer = Volunteer.find_by_id(id)
        volunteer.accepted = False
        meta.Session.commit()
        h.flash('Status Updated')
        redirect_to(action='index')
