from zookeepr.tests.model import *

class TestAccomodationLocationTable(TableTest):
    """Test the ``accommodation_location`` table.

    This table stores accommodation locations.
    """
    table = model.registration.tables.accommodation_location
    samples = [dict(name='foo college',
                    beds=1),
               dict(name='bar college',
                    beds=2),
               ]
    not_nullables = ['name', 'beds']
    uniques = ['name']
