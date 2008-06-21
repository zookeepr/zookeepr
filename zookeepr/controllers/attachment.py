from zookeepr.lib.auth import SecureController, AuthRole, AuthTrue, AuthFunc
from zookeepr.lib.base import *
from zookeepr.lib.crud import Delete
from zookeepr.model import Attachment, Proposal

class AttachmentController(SecureController, Delete):
    model = Attachment
    individual = 'attachment'

    permissions = {
      'view': True,
      'delete': [AuthFunc('is_submitter'), AuthRole('organiser')]
    }

    def delete(self, id):
        if request.method == 'POST' and self.obj is not None:
            self.dbsession.delete(self.obj)
            self.dbsession.flush()

            proposal = self.dbsession.query(model.Proposal).get(self.obj.proposal_id)
            redirect = dict(controller='proposal', action='view', id=session.get('proposal_id', proposal.id))
            self.redirect_to('delete', redirect)

        # call the template
        return render_response('%s/confirm_delete.myt' % self.individual)

    def is_submitter(self):
        proposal = self.dbsession.query(model.Proposal).get(self.obj.proposal_id)
        if c.signed_in_person in proposal.people:
            return True
        else:
            return False

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
