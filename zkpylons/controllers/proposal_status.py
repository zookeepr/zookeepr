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
from zkpylons.model.proposal import ProposalStatus

log = logging.getLogger(__name__)

class ProposalStatusSchema(BaseSchema):
    name = validators.String(not_empty=True)

class NewProposalStatusSchema(BaseSchema):
    proposal_status = ProposalStatusSchema()
    pre_validators = [NestedVariables]

class EditProposalStatusSchema(BaseSchema):
    proposal_status = ProposalStatusSchema()
    pre_validators = [NestedVariables]

class ProposalStatusController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        c.can_edit = True

    @dispatch_on(POST="_new")
    def new(self):
        return render('/proposal_status/new.mako')

    @validate(schema=NewProposalStatusSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['proposal_status']

        c.proposal_status = ProposalStatus(**results)
        meta.Session.add(c.proposal_status)
        meta.Session.commit()

        h.flash("Proposal Status created")
        redirect_to(action='index', id=None)

    def view(self, id):
        c.proposal_status = ProposalStatus.find_by_id(id)
        return render('/proposal_status/view.mako')

    def index(self):
        c.proposal_status_collection = ProposalStatus.find_all()
        return render('/proposal_status/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.proposal_status = ProposalStatus.find_by_id(id)

        defaults = h.object_to_defaults(c.proposal_status, 'proposal_status')

        form = render('/proposal_status/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditProposalStatusSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        proposal_status = ProposalStatus.find_by_id(id)

        for key in self.form_result['proposal_status']:
            setattr(proposal_status, key, self.form_result['proposal_status'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Proposal Status has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the proposal_status

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.proposal_status = ProposalStatus.find_by_id(id)
        return render('/proposal_status/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.proposal_status = ProposalStatus.find_by_id(id)
        meta.Session.delete(c.proposal_status)
        meta.Session.commit()

        h.flash("Proposal Status has been deleted.")
        redirect_to('index')
