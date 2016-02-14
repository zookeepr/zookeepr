import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model.travel import Travel

log = logging.getLogger(__name__)

class TravelSchema(BaseSchema):
    origin_airport = validators.String(not_empty=True)
    destination_airport = validators.String(not_empty=True)
    flight_details = validators.String(if_missing="")

class NewTravelSchema(BaseSchema):
    travel = TravelSchema()
    pre_validators = [NestedVariables]

class EditTravelSchema(BaseSchema):
    travel = TravelSchema()
    pre_validators = [NestedVariables]

class TravelController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    @authorize(h.auth.has_funding_reviewer_role)
    def __before__(self, **kwargs):
        c.can_edit = True

    @dispatch_on(POST="_new")
    def new(self):
        return render('/travel/new.mako')

    @validate(schema=NewTravelSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['travel']

        # TODO: This doesn't make sense, Travel controller is restricted to admins
        #       But new template refers to each person updating their details
        c.travel = Travel(**results)
        c.travel.person = h.signed_in_person()
        meta.Session.add(c.travel)
        meta.Session.commit()

        h.flash("Travel created")
        redirect_to(action='index', id=None)

    def view(self, id):
        c.travel = Travel.find_by_id(id)
        return render('/travel/view.mako')

    def index(self):
        c.travel_collection = Travel.find_all()
        return render('/travel/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.travel = Travel.find_by_id(id)

        defaults = h.object_to_defaults(c.travel, 'travel')

        form = render('/travel/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditTravelSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        travel = Travel.find_by_id(id)

        for key in self.form_result['travel']:
            setattr(travel, key, self.form_result['travel'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Travel has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the travel

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.travel = Travel.find_by_id(id)
        return render('/travel/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.travel = Travel.find_by_id(id)
        meta.Session.delete(c.travel)
        meta.Session.commit()

        h.flash("Travel has been deleted.")
        redirect_to('index')
