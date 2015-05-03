import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, DictSet, ProductValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import ProductCategory
from zkpylons.model.product import Product
from zkpylons.model.volunteer import Volunteer

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

class AcceptVolunteerSchema(BaseSchema):
    ticket_type = ProductValidator()

class VolunteerController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.is_valid_user)
    @authorize(h.auth.is_activated_user)
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
        c.person = c.volunteer.person
        meta.Session.add(c.volunteer)
        meta.Session.commit()

        h.flash("Thank you for volunteering. We will contact you shortly regarding your application")
        email(c.person.email_address, render('volunteer/response.mako'))
        redirect_to(action='view', id=c.volunteer.id)

    @dispatch_on(POST="_edit") 
    def edit(self, id):
        # A person can only volunteer once
        c.form = 'edit'
        c.volunteer = Volunteer.find_by_id(id)
        defaults = h.object_to_defaults(c.volunteer, 'volunteer')
        form = render('/volunteer/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditVolunteerSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        results = self.form_result['volunteer']
        c.volunteer = Volunteer.find_by_id(id)
        for key in self.form_result['volunteer']:
            setattr(c.volunteer, key, self.form_result['volunteer'][key])
        meta.Session.commit()
        redirect_to(action='view', id=c.volunteer.id)

    def view(self, id):
        c.volunteer = Volunteer.find_by_id(id)

        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(c.volunteer.person.id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.can_edit = h.auth.is_same_zkpylons_user(c.volunteer.person.id)

        c.volunteer = Volunteer.find_by_id(id)
        if c.volunteer is None:
            abort(404, "No such object")

        return render('volunteer/view.mako')

    def index(self):
        # Check access and redirect
        if not h.auth.authorized(h.auth.has_organiser_role):
            redirect_to(action='new')

        c.volunteer_collection = Volunteer.find_all()
        return render('volunteer/list.mako')

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_accept")
    def accept(self, id):
        volunteer = Volunteer.find_by_id(id)
        category = ProductCategory.find_by_name('Ticket')
        products = Product.find_by_category(category.id)
        defaults = {}
        if volunteer.ticket_type:
            defaults['ticket_type'] = volunteer.ticket_type.id
        c.products_select = []
        c.products_select.append(['', 'No Ticket'])
        for p in products:
            if 'Volunteer' in p.description:
                c.products_select.append([p.id, p.description + ' - ' + h.integer_to_currency(p.cost)])
        form = render('volunteer/accept.mako') 
        return htmlfill.render(form, defaults)

    @authorize(h.auth.has_organiser_role)
    @validate(schema=AcceptVolunteerSchema(), form='accept', post_only=True, on_get=True, variable_decode=True)
    def _accept(self, id):
        results = self.form_result
        volunteer = Volunteer.find_by_id(id)
        volunteer.ticket_type = results['ticket_type']
        volunteer.accepted = True
        meta.Session.commit()
        c.volunteer = volunteer
        c.person = volunteer.person
        email(c.person.email_address, render('volunteer/response.mako'))
        h.flash('Status Updated and Acceptance Email Sent')
        redirect_to(action='index', id=None)

    @authorize(h.auth.has_organiser_role)
    def pending(self, id):
        volunteer = Volunteer.find_by_id(id)
        volunteer.accepted = None
        volunteer.ticket_type = None
        meta.Session.commit()
        h.flash('Status Updated')
        redirect_to(action='index', id=None)

    @authorize(h.auth.has_organiser_role)
    def reject(self, id):
        volunteer = Volunteer.find_by_id(id)
        volunteer.accepted = False
        volunteer.ticket_type = None
        meta.Session.commit()
        c.volunteer = volunteer
        c.person = volunteer.person
        email(c.person.email_address, render('volunteer/response.mako'))
        h.flash('Status Updated and Rejection Email Sent')
        redirect_to(action='index', id=None)
