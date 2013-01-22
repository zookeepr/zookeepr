import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, ExistingPersonValidator, FulfilmentTypeValidator, FulfilmentStatusValidator, FulfilmentTypeStatusValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta, Fulfilment, FulfilmentType, FulfilmentStatus, FulfilmentGroup, Person

from zkpylons.config.lca_info import lca_info

log = logging.getLogger(__name__)

class FulfilmentSchema(BaseSchema):
    person = ExistingPersonValidator()
    type = FulfilmentTypeValidator(not_empty=True)
    status = FulfilmentStatusValidator(not_empty=True)
    chained_validators = [FulfilmentTypeStatusValidator(type='type', status='status')]

class NewFulfilmentSchema(BaseSchema):
    fulfilment = FulfilmentSchema()
    pre_validators = [NestedVariables]

class EditFulfilmentSchema(BaseSchema):
    fulfilment = FulfilmentSchema()
    pre_validators = [NestedVariables]

class FulfilmentController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        c.can_edit = True

        c.fulfilment_type = FulfilmentType.find_all()
        c.fulfilment_status = FulfilmentStatus.find_all()

    @dispatch_on(POST="_new")
    def new(self):
        return render('/fulfilment/new.mako')

    @validate(schema=NewFulfilmentSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['fulfilment']

        c.fulfilment = Fulfilment(**results)
        meta.Session.add(c.fulfilment)
        meta.Session.commit()

        h.flash("Fulfilment created")
        redirect_to(action='index', id=None)

    def view(self, id):
        c.fulfilment = Fulfilment.find_by_id(id)
        return render('/fulfilment/view.mako')

    def person(self, id):
        c.person = Person.find_by_id(id)
        return render('/fulfilment/person.mako')

    def index(self):
        c.fulfilment_collection = Fulfilment.find_all()
        return render('/fulfilment/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.fulfilment = Fulfilment.find_by_id(id)

        defaults = h.object_to_defaults(c.fulfilment, 'fulfilment')
        defaults['fulfilment.person'] = c.fulfilment.person_id
        defaults['fulfilment.type'] = c.fulfilment.type_id
        defaults['fulfilment.status'] = c.fulfilment.status_id

        form = render('/fulfilment/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditFulfilmentSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        fulfilment = Fulfilment.find_by_id(id)

        for key in self.form_result['fulfilment']:
            setattr(fulfilment, key, self.form_result['fulfilment'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Fulfilment has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the fulfilment

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.fulfilment = Fulfilment.find_by_id(id)
        return render('/fulfilment/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.fulfilment = Fulfilment.find_by_id(id)
        meta.Session.delete(c.fulfilment)
        meta.Session.commit()

        h.flash("Fulfilment has been deleted.")
        redirect_to('index', id=None)
