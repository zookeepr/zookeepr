"""populate lookup tables

Revision ID: 4cb574d6501a
Revises: 58ee75910929
Create Date: 2016-01-24 15:10:59.528914

"""

# revision identifiers, used by Alembic.
revision = '4cb574d6501a'
down_revision = '58ee75910929'

import logging
from alembic import op
import sqlalchemy as sa

meta = sa.MetaData()
log = logging.getLogger('alembic.migration')

tables = [
    'event_type',
    'fulfilment_status',
    'fulfilment_type',
    'fulfilment_type_status_map',
]

tables_delete_order = [
    'event_type',
    'fulfilment_type_status_map',
    'fulfilment_type',
    'fulfilment_status',
]

data = {
    'event_type' : [
        {
            'id' : 1,
            'name' : 'presentation',
        },
        {
            'id' : 2,
            'name' : 'plenary',
        },
        {
            'id' : 3,
            'name' : 'break',
        },
        {
            'id' : 4,
            'name' : 'social',
        },
        {
            'id' : 5,
            'name' : 'heading',
        },
    ],
    'fulfilment_status' : [
        {
            'id' : 3,
            'name' : 'Completed',
            'locked' : False,
            'void' : False,
            'completed' : True,
        },
        {
            'id' : 2,
            'name' : 'Bag Drop Pending',
            'locked' : True,
            'void' : False,
            'completed' : False,
        },
        {
            'id' : 7,
            'name' : 'Cancelled',
            'locked' : False,
            'void' : True,
            'completed' : False,
        },
        {
            'id' : 9,
            'name' : 'Pre-Printed',
            'locked' : True,
            'void' : False,
            'completed' : False,
        },
        {
            'id' : 6,
            'name' : 'Collected',
            'locked' : False,
            'void' : False,
            'completed' : True,
        },
        {
            'id' : 5,
            'name' : 'Printed',
            'locked' : False,
            'void' : False,
            'completed' : True,
        },
        {
            'id' : 10,
            'name' : 'Print - Boarding Pass',
            'locked' : True,
            'void' : False,
            'completed' : False,
        },
        {
            'id' : 11,
            'name' : 'Print - Please Check',
            'locked' : False,
            'void' : False,
            'completed' : False,
            },
        {
            'id' : 1,
            'name' : 'Give out - No Bag',
            'locked' : False,
            'void' : False,
            'completed' : False,
        },
        {
            'id' : 4,
            'name' : 'Give out',
            'locked' : True,
            'void' : False,
            'completed' : False,
        },
        {
            'id' : 12,
            'name' : 'Check-in',
            'locked' : False,
            'void' : False,
            'completed' : False,
        },
    ],
    'fulfilment_type' : [
        {
            'id' : 1,
            'name' : 'Accommodation',
            'initial_status_id' : 12,
        },
        {
            'id' : 2,
            'name' : 'Badge',
            'initial_status_id' : 11,
        },
        {
            'id' : 3,
            'name' : 'Partners\' Programme',
            'initial_status_id' : 1,
        },
        {
            'id' : 4,
            'name' : 'Swag',
            'initial_status_id' : 1,
        },
    ],
    'fulfilment_type_status_map' : [
        {
            'fulfilment_type_id' : 1,
            'fulfilment_status_id' : 1,
        },
        {
            'fulfilment_type_id' : 2,
            'fulfilment_status_id' : 1,
        },
        {
            'fulfilment_type_id' : 3,
            'fulfilment_status_id' : 1,
        },
        {
            'fulfilment_type_id' : 4,
            'fulfilment_status_id' : 1,
        },
        {
            'fulfilment_type_id' : 4,
            'fulfilment_status_id' : 2,
        },
        {
            'fulfilment_type_id' : 4,
            'fulfilment_status_id' : 3,
        },
        {
            'fulfilment_type_id' : 4,
            'fulfilment_status_id' : 4,
        },
        {
            'fulfilment_type_id' : 4,
            'fulfilment_status_id' : 5,
        },
        {
            'fulfilment_type_id' : 2,
            'fulfilment_status_id' : 6,
        },
        {
            'fulfilment_type_id' : 4,
            'fulfilment_status_id' : 7,
        },
        {
            'fulfilment_type_id' : 2,
            'fulfilment_status_id' : 7,
        },
        {
            'fulfilment_type_id' : 3,
            'fulfilment_status_id' : 6,
        },
        {
            'fulfilment_type_id' : 2,
            'fulfilment_status_id' : 9,
        },
        {
            'fulfilment_type_id' : 2,
            'fulfilment_status_id' : 10,
        },
        {
            'fulfilment_type_id' : 2,
            'fulfilment_status_id' : 11,
        },
        {
            'fulfilment_type_id' : 1,
            'fulfilment_status_id' : 12,
        },
    ],
}

def insert_rows(connection, table_name):
    log.info('Loading data for {0}'.format(table_name))
    table = sa.schema.Table(
        table_name, meta, autoload=True, autoload_with=connection)
    connection.execute(table.insert().values(data[table_name]))

    # Insertions specify id numbers, because some code has hardcoded ids
    # However doing this messes up the automatic sequence, so we correct it
    # This will fail messily for a non-postgres database
    if 'id' in data[table_name][0]:
        sequence_name = "%s_id_seq" % table_name
        # Manually selecting from sequence is easier to handle if table was empty
        curr_id = connection.execute("SELECT last_value FROM %s" % sequence_name).scalar()
        new_id = curr_id + len(data[table_name])
        log.info('Correcting id sequence for {0}, {1} -> {2}'.format(table_name, curr_id, new_id))
        connection.execute("SELECT setval('%s', %d)" % (sequence_name, new_id))
    else:
        log.info('Correcting id sequence for {0} not required'.format(table_name))
        



def delete_rows(connection, table_name):
    log.info('Deleting data from {0}'.format(table_name))
    table = sa.schema.Table(
        table_name, meta, autoload=True, autoload_with=connection)
    connection.execute(table.delete())


def upgrade():
    connection = op.get_bind()

    for table in tables:
        insert_rows(connection, table)


def downgrade():
    connection = op.get_bind()

    for table in tables_delete_order:
        delete_rows(connection, table)
