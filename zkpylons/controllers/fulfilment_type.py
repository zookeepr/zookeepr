import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, FulfilmentStatusValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta, FulfilmentStatus, FulfilmentType

from zkpylons.config.lca_info import lca_info

log = logging.getLogger(__name__)

class FulfilmentTypeSchema(BaseSchema):
    name = validators.String(not_empty=True)
    initial_status = FulfilmentStatusValidator(not_empty=True)
    status = ForEach(FulfilmentStatusValidator())

class NewFulfilmentTypeSchema(BaseSchema):
    fulfilment_type = FulfilmentTypeSchema()
    pre_validators = [NestedVariables]

class EditFulfilmentTypeSchema(BaseSchema):
    fulfilment_type = FulfilmentTypeSchema()
    pre_validators = [NestedVariables]

class FulfilmentTypeController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        c.can_edit = True
        c.fulfilment_status = FulfilmentStatus.find_all()

    @dispatch_on(POST="_new")
    def new(self):
        return render('/fulfilment_type/new.mako')

    @validate(schema=NewFulfilmentTypeSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['fulfilment_type']

        c.fulfilment_type = FulfilmentType(**results)
        meta.Session.add(c.fulfilment_type)
        meta.Session.commit()

        h.flash("Fulfilment Type created")
        redirect_to(action='index', id=None)

    def view(self, id):
        c.fulfilment_type = FulfilmentType.find_by_id(id)
        return render('/fulfilment_type/view.mako')

    def index(self):
        c.fulfilment_type_collection = FulfilmentType.find_all()
        return render('/fulfilment_type/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.fulfilment_type = FulfilmentType.find_by_id(id)

        defaults = h.object_to_defaults(c.fulfilment_type, 'fulfilment_type')
        defaults['fulfilment_type.initial_status'] = c.fulfilment_type.initial_status_id
        defaults['fulfilment_type.status'] = [s.id for s in c.fulfilment_type.status]


        form = render('/fulfilment_type/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditFulfilmentTypeSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        fulfilment_type = FulfilmentType.find_by_id(id)

        for key in self.form_result['fulfilment_type']:
            setattr(fulfilment_type, key, self.form_result['fulfilment_type'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The FulfilmentType has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the fulfilment_type

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.fulfilment_type = FulfilmentType.find_by_id(id)
        return render('/fulfilment_type/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.fulfilment_type = FulfilmentType.find_by_id(id)
        meta.Session.delete(c.fulfilment_type)
        meta.Session.commit()

        h.flash("FulfilmentType has been deleted.")
        redirect_to('index', id=None)
