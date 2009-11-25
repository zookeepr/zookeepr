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
    areas = DictSet(not_empty=True)
    other = validators.String()
    experience = validators.String()

class NewVolunteerSchema(BaseSchema):
    volunteer = VolunteerSchema()
    pre_validators = [NestedVariables]

class EditVolunteerSchema(BaseSchema):
    volunteer = VolunteerSchema()
    pre_validators = [NestedVariables]

class VolunteerController(BaseController):

    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        # A person can only volunteer once
        if h.signed_in_person() and h.signed_in_person().volunteer:
            return redirect_to(action='edit', id=h.signed_in_person().volunteer.id)

        return render('/volunteer/new.mako')

    @validate(schema=NewVolunteerSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['volunteer']

        c.volunteer = Volunteer(**results)
        c.volunteer.person = h.signed_in_person()
        meta.Session.add(c.volunteer)
        meta.Session.commit()

        h.flash("Volunteer application submitted. Thank you for your interest.")
        redirect_to(action='view', id=c.volunteer.id)

    def view(self, id):
        c.volunteer = Volunteer.find_by_id(id)

        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(c.volunteer.person.id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.can_edit = h.auth.is_same_zookeepr_user(c.volunteer.person.id)

        c.volunteer = Volunteer.find_by_id(id)
        if c.volunteer is None:
            abort(404, "No such object")

        return render('volunteer/view.mako')

    @authorize(h.auth.has_organiser_role)
    def index(self):
        # Check access and redirect
        if not h.auth.has_organiser_role:
            redirect_to(action='new')

        c.volunteer_collection = Volunteer.find_all()
        return render('volunteer/list.mako')

    @authorize(h.auth.has_organiser_role)
    def grid(self):
        # Check access and redirect
        if not h.auth.has_organiser_role:
            redirect_to(action='new')


        c.data = []
        c.noescape = True
        c.columns = ['Name', 'Email']
        for area in h.lca_rego['volunteer_areas']:
          c.columns.append(area['name'])
        c.columns.append('Other')
        c.columns.append('Experience')

        volunteer_collection = Volunteer.find_all()
        for v in volunteer_collection:
          row = [h.link_to(v.person.fullname(), url=h.url_for(controller="person", action='view', id=v.person.id))]
          row.append(h.link_to(v.person.email_address, url="mailto:" + v.person.email_address))
          
          for area in h.lca_rego['volunteer_areas']:
            code = area['name'].replace(' ', '_').replace('.', '_')
            if code in v.areas:
              row.append('Yes')
            else:
              row.append('No')

          row.append(v.other)
          row.append(v.experience)

          c.data.append(row)

        return render('/admin/table.mako')

    @dispatch_on(POST="_edit") 
    def edit(self, id):
        c.volunteer = Volunteer.find_by_id(id)

        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(c.volunteer.person.id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        if c.volunteer.accepted is not None:
            return render('volunteer/already.mako')

        defaults = h.object_to_defaults(c.volunteer, 'volunteer')

        form = render('volunteer/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditVolunteerSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        volunteer = Volunteer.find_by_id(id)

        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(volunteer.person.id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

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
