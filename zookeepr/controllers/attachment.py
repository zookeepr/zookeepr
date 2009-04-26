import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, ProductValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model import Attachment, Proposal

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)

class AttachmentController(BaseController):
    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_delete")
    def delete(self, id):
        c.attachment = Attachment.find_by_id(id)
        author_id = c.attachment.proposal.person.id

        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(author_id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()
        return render_response('/attachment/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True)
    def _delete(self, id):
        c.attachment = Attachment.find_by_id(id)
        author_id = c.attachment.proposal.person.id

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(author_id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        proposal_id = c.attachment.proposal.id
        meta.Session.delete(c.attachment)
        meta.Session.commit()

        h.flash("Attachment Deleted")
        redirect_to(controller='proposal', action='view', id=proposal_id)

    def view(self, id):
        attachment = Attachment.find_by_id(id)
        author_id = attachment.proposal.person.id

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(author_id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        response = Response(attachment.content)
        response.headers['content-type'] = attachment.content_type
        response.headers.add('content-transfer-encoding', 'binary')
        response.headers.add('content-length', len(attachment.content))
        response.headers['content-disposition'] = 'attachment; filename="%s";' % attachment.filename

        response.headers.add('Pragma', 'cache')
        response.headers.add('Cache-Control', 'max-age=3600,public')

        return response
