from zookeepr.tests.model import *

class TestAccommodationTable(TableTest):
    """Test the ``accommodation`` table.

    This table stores accommodation details.
    """
    table = model.registration.tables.accommodation
    samples = [dict(name='name1',
                    cost_per_night=1,
                    beds=1,
                    ),
               dict(name='name2',
                    cost_per_night=2,
                    beds=2,
                    )
               ]
