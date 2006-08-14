from zookeepr.tests.model import *

class TestPerson(TableTest):
    """Test the ``person`` table.

    This table stores auxiliary information about a person: their name,
    their contact details, etc, and references an account table that
    contains the person's login details.
    """
    table = 'core.tables.person'
    samples = [dict(handle='testguy',
                    firstname='Testguy',
                    lastname='McTest',
                    phone='+61295555555',
                    fax='+61295555556',
                    account_id=1,
                    ),
               dict(handle='testgirl',
                    firstname='Testgirl',
                    lastname='Van Test',
                    phone='+37',
                    fax='42',
                    account_id=2,
                    ),
               ]
    uniques = ['handle']
