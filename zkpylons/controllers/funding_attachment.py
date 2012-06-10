import logging

from pylons import request, response, session, tmpl_context as c
from zookeepr.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model import Funding, FundingAttachment

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)

class FundingAttachmentController(BaseController):
    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_delete")
    def delete(self, id):
        c.attachment = FundingAttachment.find_by_id(id)
        c.funding = Funding.find_by_id(c.attachment.funding_id)
        
        if not (h.auth.authorized(h.auth.has_organiser_role) or c.funding.person == h.signed_in_person()):
            # Raise a no_auth error
            h.auth.no_role()

        return render('/funding_attachment/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.attachment = FundingAttachment.find_by_id(id)
        funding = Funding.find_by_id(c.attachment.funding_id)

        if not (h.auth.authorized(h.auth.has_organiser_role) or funding.person == h.signed_in_person()):
            # Raise a no_auth error
            h.auth.no_role()

        meta.Session.delete(c.attachment)
        meta.Session.commit()

        h.flash("Attachment Deleted")
        redirect_to(controller='funding', action='view', id=funding.id)

    def view(self, id):
        attachment = FundingAttachment.find_by_id(id)
        funding = Funding.find_by_id(attachment.funding_id)

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_funding_submitter(funding.id), h.auth.has_organiser_role, h.auth.has_funding_reviewer_role)):
            # Raise a no_auth error
            h.auth.no_role()

        response.headers['content-type'] = attachment.content_type
        response.headers.add('content-transfer-encoding', 'binary')
        response.headers.add('content-length', len(attachment.content))
        response.headers['content-disposition'] = 'attachment; filename="%s";' % attachment.filename
        response.headers.add('Pragma', 'cache')
        response.headers.add('Cache-Control', 'max-age=3600,public')
        return attachment.content
