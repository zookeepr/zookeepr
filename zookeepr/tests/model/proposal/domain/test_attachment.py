import datetime

from zookeepr.tests.model import *

class TestAttachmentModel(CRUDModelTest):
    domain = model.proposal.Attachment
    samples = [dict(filename='attachment 1',
                    content_type='text/plain',
                    creation_timestamp=datetime.datetime(2006,8,29,16,23,37),
                    content="some text"),
               dict(filename='attach 2',
                    content_type='application/octet-stream',
                    creation_timestamp=datetime.datetime(2006,8,29,16,24,37),
                    content="some more different text"),
               ]
    mangles = {'content': lambda t: buffer(t)}

    def setUp(self):
        super(TestAttachmentModel, self).setUp()
        self.p = model.Proposal(title='a', abstract='b')
        objectstore.save(self.p)
        objectstore.flush()
        self.pid = self.p.id

    def tearDown(self):
        objectstore.delete(Query(model.Proposal).get(self.pid))
        objectstore.flush()
        super(TestAttachmentModel, self).tearDown()

    def additional(self, obj):
        self.p.attachments.append(obj)
        return obj
