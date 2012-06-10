from zkpylons.tests.model import *

class TestAttachmentTable(TableTest):
    """Test the ``attachment`` table.

    This table stores attachments: their names, content-type, upload
    time, and content.
    """
    table = model.proposal.tables.attachment
    samples = [dict(_filename='test',
                    proposal_id=1,
                    _content_type='application/octet-stream',
                    content=buffer("foo")),
               dict(_filename='test2',
                    proposal_id=2,
                    _content_type='text/plain',
                    content=buffer("bar")),
               ]
    not_nullables = ['_filename', '_content_type', 'content']
