from zookeepr.lib.auth import BaseController, AuthRole, AuthTrue, AuthFunc
from zookeepr.lib.base import *
from zookeepr.lib.crud import Delete
from zookeepr.model import Attachment, Proposal

class AttachmentController(BaseController):
    @authorize(h.auth.is_valid_user)
    @dispatch_on(POST="_delete")
    def delete(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()
        return render_response('/attachment/confirm_delete.mako')

    @authorize(h.auth.is_valid_user)
    def _delete(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.attachment = Attachment.find_by_id(id)
        proposal_id = c.attachment.proposal.id
        meta.Session.delete(c.attachment)
        meta.Session.commit()

        h.flash("Attachment Deleted")
        redirect_to(controller='proposal', action='view', id=proposal_id)

    def view(self, id):
        att = self.dbsession.query(model.Attachment).get(id)

        response = Response(att.content)
        response.headers['content-type'] = att.content_type
        response.headers.add('content-transfer-encoding', 'binary')
        response.headers.add('content-length', len(att.content))
        response.headers['content-disposition'] = 'attachment; filename="%s";' % att.filename

        response.headers.add('Pragma', 'cache')
        response.headers.add('Cache-Control', 'max-age=3600,public')

        return response
