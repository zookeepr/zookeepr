from sqlalchemy import *

from zookeepr.model import metadata

print func, dir(func)
print func.current_timestamp, dir(func.current_timestamp)

invoice = Table('invoice', metadata,
                Column('id', Integer, primary_key=True),

                Column('person_id', Integer,
                       ForeignKey('person.id'),
                       nullable=False,
                       ),

                Column('issue_date', DateTime,
                       default=func.current_timestamp(),
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
                     Column('cost', Integer,
                            nullable=False),
                     )

payment = Table('payment', metadata,
                Column('id', Integer, primary_key=True),

                Column('invoice_id', Integer,
                       ForeignKey('invoice.id'),
                       nullable=False),
                
                Column('amount', Integer,
                       nullable=False),
                )

payment_received = Table('payment_received', metadata,
                         Column('id', Integer, primary_key=True),

                         Column('invoice_id', Integer,
                                ForeignKey('invoice.id'),
                                key='InvoiceID',
                                ),

                         Column('payment_id', Integer,
                                ForeignKey('payment.id'),
                                key='PaymentID',
                                ),

                         Column('auth_num', Integer,
                                key='AuthNum',
                                ),
                         Column('amount', Integer,
                                key='Amount',
                                ),
                         Column('refund_key', String,
                                key='RefundKey',
                                ),
                         Column('merchant_id', String,
                                key='MerchantID',
                                ),
                         Column('status', String,
                                key='Status',
                                ),
                         Column('settlement', Integer,
                                key='Settlement'),
                         Column('error_string', String,
                                key='ErrorString',
                                ),
                         Column('card_name', String,
                                key='CardName',
                                ),
                         Column('requested_page', String,
                                key='RequestedPage',
                                ),
                         Column('card_type', String,
                                key='CardType',
                                ),
                         Column('mac', String,
                                key='MAC',
                                ),
                         Column('card_number', String,
                                key='CardNumber',
                                ),
                         Column('trans_id', String,
                                key='TransID',
                                ),
                         Column('original_amount', Integer,
                                key='ORIGINAL_AMOUNT',
                                ),
                         Column('surcharge', Integer,
                                key='Surcharge',
                                ),
                         Column('result', String,
                                key='result',
                                ),
                         )
