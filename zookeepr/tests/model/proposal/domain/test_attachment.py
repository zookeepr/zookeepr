import datetime

from zookeepr.tests.model import *

class TestAttachmentModel(CRUDModelTest):
    model = 'proposal.Attachment'
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
