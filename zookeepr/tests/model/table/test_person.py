from zookeepr.tests.model.table import *

class TestPerson(TableTest):
    """Test the ``person`` table.

    This table stores auxiliary information about a person: their name,
    their contact details, etc, and references an account table that
    contains the person's login details.
    """
    table = 'core.tables.person'
    samples = [dict(handle='testguy',
                    account_id=1,
                    firstname='Testguy',
                    lastname='McTest',
                    phone='+61295555555',
                    fax='+61295555556',
                    ),
               dict(handle='testgirl',
                    account_id=2,
                    firstname='Testgirl',
                    lastname='Van Test',
                    phone='+37',
                    fax='42',
                    )
               ]
    uniques = ['handle']
