import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, FulfilmentTypeValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta, FulfilmentStatus, FulfilmentType

from zkpylons.config.lca_info import lca_info

log = logging.getLogger(__name__)

class FulfilmentStatusSchema(BaseSchema):
    name = validators.String(not_empty=True)
    void = validators.Bool(if_missing=False)
    completed = validators.Bool(if_missing=False)
    locked = validators.Bool(if_missing=False)
    types = ForEach(FulfilmentTypeValidator())

class NewFulfilmentStatusSchema(BaseSchema):
    fulfilment_status = FulfilmentStatusSchema()
    pre_validators = [NestedVariables]

class EditFulfilmentStatusSchema(BaseSchema):
    fulfilment_status = FulfilmentStatusSchema()
    pre_validators = [NestedVariables]

class FulfilmentStatusController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        c.can_edit = True
        c.fulfilment_types = FulfilmentType.find_all()

    @dispatch_on(POST="_new")
    def new(self):
        return render('/fulfilment_status/new.mako')

    @validate(schema=NewFulfilmentStatusSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['fulfilment_status']

        c.fulfilment_status = FulfilmentStatus(**results)
        meta.Session.add(c.fulfilment_status)
        meta.Session.commit()

        h.flash("Fulfilmnet Status created")
        redirect_to(action='index', id=None)

    def view(self, id):
        c.fulfilment_status = FulfilmentStatus.find_by_id(id)
        return render('/fulfilment_status/view.mako')

    def index(self):
        c.fulfilment_status_collection = FulfilmentStatus.find_all()
        return render('/fulfilment_status/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.fulfilment_status = FulfilmentStatus.find_by_id(id)

        defaults = h.object_to_defaults(c.fulfilment_status, 'fulfilment_status')
        defaults['fulfilment_status.types'] = [t.id for t in c.fulfilment_status.types]

        form = render('/fulfilment_status/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditFulfilmentStatusSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        fulfilment_status = FulfilmentStatus.find_by_id(id)

        for key in self.form_result['fulfilment_status']:
            setattr(fulfilment_status, key, self.form_result['fulfilment_status'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Fulfilment Status has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the fulfilment_status

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.fulfilment_status = FulfilmentStatus.find_by_id(id)
        return render('/fulfilment_status/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.fulfilment_status = FulfilmentStatus.find_by_id(id)
        meta.Session.delete(c.fulfilment_status)
        meta.Session.commit()

        h.flash("Fulfilment Status has been deleted.")
        redirect_to('index', id=None)
