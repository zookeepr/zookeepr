from zookeepr.tests.model import *

class TestAccommodationOptionTable(TableTest):
    """Test the ``accommodation_option`` table.

    This table stores accommodation options and costs.
    """
    table = model.registration.tables.accommodation_option
    samples = [dict(name='',
                    accommodation_location_id=1,
                    cost_per_night=1.0),
               dict(name='breakfast',
                    accommodation_location_id=2,
                    cost_per_night=2.0),
               ]
    not_nullables = ['cost_per_night', 'accommodation_location_id']
