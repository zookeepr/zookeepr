import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema, ProductValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model.special_offer import SpecialOffer
from zkpylons.model.special_registration import SpecialRegistration

log = logging.getLogger(__name__)

class NotExistingSpecialOfferValidator(validators.FancyValidator):
    def validate_python(self, values, state):
        special_offer = SpecialOffer.find_by_name(values['special_offer']['name'])
        if special_offer != None and special_offer != c.special_offer:
	    message = "Duplicate Special Offer name"
	    error_dict = {'special_offer.name': "Special Offer name already in use"}
	    raise Invalid(message, values, state, error_dict=error_dict)

class SpecialOfferSchema(BaseSchema):
    enabled = validators.Bool(if_empty=False)
    name = validators.String(not_empty=True)
    description = validators.String(not_empty=True)
    id_name = validators.String(not_empty=True)

class NewSpecialOfferSchema(BaseSchema):
    special_offer = SpecialOfferSchema()
    pre_validators = [NestedVariables]
    chained_validators = [NotExistingSpecialOfferValidator()]

class EditSpecialOfferSchema(BaseSchema):
    special_offer = SpecialOfferSchema()
    pre_validators = [NestedVariables]

class SpecialOfferController(BaseController):

    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        return render('/special_offer/new.mako')

    @validate(schema=NewSpecialOfferSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['special_offer']

        c.special_offer = SpecialOffer(**results)
        meta.Session.add(c.special_offer)
        meta.Session.commit()

        h.flash("Special Offer created")
        redirect_to(action='view', id=c.special_offer.id)

    def view(self, id):
        c.special_offer = SpecialOffer.find_by_id(id)
        c.registrations = SpecialRegistration.find_by_offer(id)
        return render('/special_offer/view.mako')

    def index(self):
        c.can_edit = True
        c.special_offer_collection = SpecialOffer.find_all()
        return render('/special_offer/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.special_offer = SpecialOffer.find_by_id(id)

        defaults = h.object_to_defaults(c.special_offer, 'special_offer')

        form = render('/special_offer/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditSpecialOfferSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        special_offer = SpecialOffer.find_by_id(id)

        for key in self.form_result['special_offer']:
            setattr(special_offer, key, self.form_result['special_offer'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The special_offer has been updated successfully.")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete") 
    def delete(self, id):
        """Delete the special_offer

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.special_offer = SpecialOffer.find_by_id(id)
        return render('/special_offer/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.special_offer = SpecialOffer.find_by_id(id)
        meta.Session.delete(c.special_offer)
        meta.Session.commit()

        h.flash("Special Offer has been deleted.")
        redirect_to('index')
