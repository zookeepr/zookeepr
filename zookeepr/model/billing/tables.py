from sqlalchemy import *

from zookeepr.model import metadata

invoice = Table('invoice', metadata,
                Column('id', Integer, primary_key=True),

                Column('person_id', Integer,
                       ForeignKey('person.id'),
                       nullable=False,
                       ),

                Column('issue_date', DateTime,
                       nullable=False),
                
                Column('creation_timestamp', DateTime,
                       nullable=False,
                       default=func.current_timestamp()),
                Column('last_modification_timestamp', DateTime,
                       nullable=False,
                       default=func.current_timestamp(),
                       onupdate=func.current_timestamp()),

                )

invoice_item = Table('invoice_item', metadata,
                     Column('id', Integer, primary_key=True),

                     Column('invoice_id', Integer,
                            ForeignKey('invoice.id'),
                            nullable=False),
                     
                     Column('description', String,
                            nullable=False),
                     Column('qty', Integer,
                            nullable=False),
                     Column('cost', Float,
                            nullable=False),
                     )

payment = Table('payment', metadata,
                Column('id', Integer, primary_key=True),

                Column('invoice_id', Integer,
                       ForeignKey('invoice.id'),
                       nullable=False),
                
                Column('amount', Float,
                       nullable=False),
                )

payment_received = Table('payment_received', metadata,
                         Column('id', Integer, primary_key=True),

                         Column('invoice_id', Integer,
                                ForeignKey('invoice.id'),
                                ),

                         Column('payment_id', Integer,
                                ForeignKey('payment.id'),
                                ),

                         Column('auth_num', Integer,
                                ),
                         Column('amount', Integer,
                                ),
                         Column('refund_key', String),
                         Column('merchant_id', String),
                         Column('status', String),
                         Column('settlement', Integer),
                         Column('error_string', String),
                         Column('card_name', String),
                         Column('requested_page', String),
                         Column('card_type', String),
                         Column('mac', String),
                         Column('card_number', String),
                         Column('trans_id', String),
                         Column('original_amount', Integer),
                         Column('surcharge', Integer),
                         )
