from zookeepr.tests.model import *

class TestOpendayTable(TableTest):
    """Test the ``registration`` table.

    This table stores registration details.
    """
    table = model.registration.tables.registration
    samples = [dict(
                    fullname='fullname1'
                    email_address='email1',
                    heardfrom='heardfrom1',
                    heardfromtext='heardfromtext1',
                    opendaydrag=1,
                dict(
                    fullname='fullname2'
                    email_address='email2',
                    heardfrom='heardfrom2',
                    heardfromtext='heardfromtext2',
                    opendaydrag=1,
                    ),
                ]
