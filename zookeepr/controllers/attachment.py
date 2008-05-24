from zookeepr.lib.auth import SecureController, AuthRole, AuthTrue
from zookeepr.lib.base import *
from zookeepr.lib.crud import Delete
from zookeepr.model import Attachment

class AttachmentController(SecureController, Delete):
    model = Attachment
    individual = 'attachment'
    redirect_map = {'delete': dict(controller='proposal', action='view', id=session.get('proposal_id', 0))}

    permissions = {
      'view': True
    }

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
