import datetime

from zookeepr.tests.model import *

class TestAttachmentTable(TableTest):
    """Test the ``attachment`` table.

    This table stores attachments: their names, content-type, upload
    time, and content.
    """
    table = 'proposal.tables.attachment'
    samples = [dict(_filename='test',
                    proposal_id=1,
                    _content_type='application/octet-stream',
                    _creation_timestamp=datetime.datetime.now(),
                    content=buffer("foo")),
               dict(_filename='test2',
                    proposal_id=2,
                    _content_type='text/plain',
                    _creation_timestamp=datetime.datetime(2006,8,29,16,13,37),
                    content=buffer("bar")),
               ]
    not_nullables = ['_filename', '_content_type', '_creation_timestamp',
                     'content']
