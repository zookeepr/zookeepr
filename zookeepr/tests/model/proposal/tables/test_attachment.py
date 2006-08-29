import datetime

from zookeepr.tests.model import *

class TestAttachmentTable(TableTest):
    """Test the ``attachment`` table.

    This table stores attachments: their names, content-type, upload
    time, and content.
    """
    table = 'proposal.tables.attachment'
    samples = [dict(name='test',
                    proposal_id=1,
                    content_type='application/octet-stream',
                    creation_timestamp=datetime.datetime.now(),
                    content=buffer("foo")),
               dict(name='test2',
                    proposal_id=2,
                    content_type='text/plain',
                    creation_timestamp=datetime.datetime(2006,8,29,16,13,37),
                    content=buffer("bar")),
               ]
    not_nullables = ['name', 'content_type', 'creation_timestamp',
                     'content']
