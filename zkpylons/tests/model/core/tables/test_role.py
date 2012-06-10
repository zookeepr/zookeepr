from zkpylons.tests.model import *

class TestRole(TableTest):
    """Test the ``role`` table.

    This table describes roles to use with an ACL system.
    """
    table = model.core.tables.role
    samples = [dict(name='test'),
               dict(name='test1'),
               ]
    not_nullables = ['name']
    uniques = ['name']
