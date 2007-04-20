from zookeepr.tests.model import *

class TestOpendayTable(TableTest):
    """Test the ``registration`` table.

    This table stores registration details.
    """
    table = model.openday.tables.openday
    samples = [dict(firstname='lastname1',
                    lastname='lastname',
                    email_address='email1',
                    heardfrom='heardfrom1',
                    heardfromtext='heardfromtext1',
                    opendaydrag=1,
                    ),
               dict(firstname='fullname2',
                    lastname='lastname2',
                    email_address='email2',
                    heardfrom='heardfrom2',
                    heardfromtext='heardfromtext2',
                    opendaydrag=1,
                    ),
                ]
