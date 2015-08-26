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

from zkpylons.model import meta, ProposalType

log = logging.getLogger(__name__)

class ProposalTypeSchema(BaseSchema):
    name = validators.String(not_empty=True)
    notify_email = validators.String(if_empty=None)

class NewProposalTypeSchema(BaseSchema):
    proposal_type = ProposalTypeSchema()
    pre_validators = [NestedVariables]

class EditProposalTypeSchema(BaseSchema):
    proposal_type = ProposalTypeSchema()
    pre_validators = [NestedVariables]

class ProposalTypeController(BaseController):
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        return render('/proposal_type/new.mako')

    @validate(schema=NewProposalTypeSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['proposal_type']

        c.proposal_type = ProposalType(**results)
        meta.Session.add(c.proposal_type)
        meta.Session.commit()

        h.flash("Proposal type created")
        redirect_to(action='view', id=c.proposal_type.id)

    def view(self, id):
        c.proposal_type = ProposalType.find_by_id(id)
        return render('/proposal_type/view.mako')

    def index(self):
        c.proposal_type_collection = ProposalType.find_all()
        return render('/proposal_type/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.proposal_type = ProposalType.find_by_id(id)

        defaults = h.object_to_defaults(c.proposal_type, 'proposal_type')

        form = render('/proposal_type/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditProposalTypeSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        proposal_type = ProposalType.find_by_id(id)

        for key in self.form_result['proposal_type']:
            setattr(proposal_type, key, self.form_result['proposal_type'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("Proposal type has been updated successfully.")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete") 
    def delete(self, id):
        """Delete the proposal type

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.proposal_type = ProposalType.find_by_id(id)
        return render('/proposal_type/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.proposal_type = ProposalType.find_by_id(id)
        meta.Session.delete(c.proposal_type)
        meta.Session.commit()

        h.flash("Proposal type has been deleted.")
        redirect_to('index')
