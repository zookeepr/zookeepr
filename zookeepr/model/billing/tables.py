from sqlalchemy import *

invoice_item = Table('invoice_item',
                     Column('id', Integer, primary_key=True),
                     
                     Column('description', String,
                            nullable=False),
                     Column('cost', Float,
                            nullable=False),
                     )

invoice = Table('invoice',
                Column('id', Integer, primary_key=True),

                Column('person_id', Integer,
                       ForeignKey('person.id'),
                       nullable=False,
                       ),
                )
