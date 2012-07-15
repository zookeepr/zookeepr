import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta, FundingType

from zkpylons.config.lca_info import lca_info

log = logging.getLogger(__name__)

class FundingTypeSchema(BaseSchema):
    name = validators.String(not_empty=True)
    active = validators.Bool(not_empty=True)
    notify_email = validators.String(if_empty=None)

class NewFundingTypeSchema(BaseSchema):
    funding_type = FundingTypeSchema()
    pre_validators = [NestedVariables]

class EditFundingTypeSchema(BaseSchema):
    funding_type = FundingTypeSchema()
    pre_validators = [NestedVariables]

class FundingTypeController(BaseController):
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        return render('/funding_type/new.mako')

    @validate(schema=NewFundingTypeSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['funding_type']

        c.funding_type = FundingType(**results)
        meta.Session.add(c.funding_type)
        meta.Session.commit()

        h.flash("Funding type created")
        redirect_to(action='view', id=c.funding_type.id)

    def view(self, id):
        c.funding_type = FundingType.find_by_id(id)
        return render('/funding_type/view.mako')

    def index(self):
        c.funding_type_collection = FundingType.find_all()
        return render('/funding_type/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.funding_type = FundingType.find_by_id(id)

        defaults = h.object_to_defaults(c.funding_type, 'funding_type')

        form = render('/funding_type/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditFundingTypeSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        funding_type = FundingType.find_by_id(id)

        for key in self.form_result['funding_type']:
            setattr(funding_type, key, self.form_result['funding_type'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("Funding type has been updated successfully.")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete") 
    def delete(self, id):
        """Delete the funding type

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.funding_type = FundingType.find_by_id(id)
        return render('/funding_type/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.funding_type = FundingType.find_by_id(id)
        meta.Session.delete(c.funding_type)
        meta.Session.commit()

        h.flash("Funding type has been deleted.")
        redirect_to('index')
