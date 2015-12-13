import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on
from pylons.controllers.util import abort

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema, ProductValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import Attachment, Proposal

log = logging.getLogger(__name__)

class AttachmentController(BaseController):
    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_delete")
    @authorize(h.auth.is_activated_user)
    def delete(self, id):
        attachment = Attachment.find_by_id(id)
        if(attachment == None): abort(400)

        authorized = h.auth.authorized(h.auth.has_organiser_role)
        for person in attachment.proposal.people:
            if h.auth.authorized(h.auth.is_same_zkpylons_user(person.id)):
                authorized = True
        if not authorized:
            # Raise a no_auth error
            h.auth.no_role()

        c.attachment = attachment
        c.proposal = attachment.proposal
        
        return render('/attachment/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        attachment = Attachment.find_by_id(id)
        if(attachment == None): abort(400)

        authorized = h.auth.authorized(h.auth.has_organiser_role)
        for person in attachment.proposal.people:
            if h.auth.authorized(h.auth.is_same_zkpylons_user(person.id)):
                authorized = True
        if not authorized:
            # Raise a no_auth error
            h.auth.no_role()

        meta.Session.delete(attachment)
        meta.Session.commit()

        h.flash("Attachment Deleted")
        redirect_to(controller='proposal', action='view', id=attachment.proposal.id)

    def view(self, id):
        attachment = Attachment.find_by_id(id)
        if(attachment == None): abort(400)

        authorized = h.auth.authorized(h.auth.has_organiser_role)
        for person in attachment.proposal.people:
            if h.auth.authorized(h.auth.is_same_zkpylons_user(person.id)):
                authorized = True
        if not authorized:
            # Raise a no_auth error
            h.auth.no_role()

        response.headers['content-type'] = attachment.content_type.encode('ascii','ignore')
        response.headers.add('content-transfer-encoding', 'binary')
        response.headers.add('content-length', len(attachment.content))
        response.headers['content-disposition'] = 'attachment; filename="%s";' % attachment.filename.encode('ascii','ignore')
        response.headers.add('Pragma', 'cache')
        response.headers.add('Cache-Control', 'max-age=3600,public')
        return attachment.content
