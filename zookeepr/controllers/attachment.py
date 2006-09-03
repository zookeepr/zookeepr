from zookeepr.lib.auth import SecureController
from zookeepr.lib.base import *
from zookeepr.lib.crud import Read
from zookeepr.model import Attachment

class AttachmentController(SecureController):
    model = Attachment
    individual = 'attachment'

    def view(self, id):
        att = g.objectstore.get(Attachment, id)

        response = Response(att.content)
        response.headers['content-type'] = att.content_type
        response.headers.add('content-transfer-encoding', 'binary')
        response.headers.add('content-length', len(att.content))
        response.headers['content-disposition'] = 'attachment; filename="%s";' % att.filename

        return response
