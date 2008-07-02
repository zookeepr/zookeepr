from sqlalchemy import *

from zookeepr.model import metadata

invoice = Table('invoice', metadata,
                Column('id', Integer, primary_key=True),

                Column('person_id', Integer,
                       ForeignKey('person.id'),
                       nullable=False,
                       ),

                Column('issue_date', DateTime,
                       default=func.current_timestamp(),
                       nullable=False),
                Column('due_date', DateTime,
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

                     Column('product_id', Integer,
                            ForeignKey('product.id'),
                            nullable=True),

                     Column('description', Text,
                            nullable=False),
                     Column('qty', Integer,
                            nullable=False),
                     Column('cost', Integer,
                            nullable=False),

                     Column('creation_timestamp', DateTime,
                            nullable=False,
                            default=func.current_timestamp()),
                     Column('last_modification_timestamp', DateTime,
                            nullable=False,
                            default=func.current_timestamp(),
                            onupdate=func.current_timestamp()),
                    )

product = Table('product', metadata,
                Column('id', Integer, primary_key=True),
                Column('description', Text, nullable=False),
                Column('cost', Integer, nullable=False),
                Column('registration', Boolean, nullable=False),
                )

product_ceiling_map = Table('product_ceiling_map', metadata,
                           Column('product_id', Integer, ForeignKey('product.id'), nullable=False),
                           Column('ceiling_id', Integer, ForeignKey('ceiling.id'), nullable=False),
                           )

ceiling = Table('ceiling', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', Text, nullable=False),
                Column('max_sold', Integer, nullable=True),
                )

payment = Table('payment', metadata,
                Column('id', Integer, primary_key=True),

                Column('invoice_id', Integer,
                       ForeignKey('invoice.id'),
                       nullable=False),

                Column('amount', Integer,
                       nullable=False),

                Column('creation_timestamp', DateTime,
                       nullable=False,
                       default=func.current_timestamp()),
                Column('last_modification_timestamp', DateTime,
                       nullable=False,
                       default=func.current_timestamp(),
                       onupdate=func.current_timestamp()),
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

                         Column('auth_num', Text,
                                key='AuthNum',
                                ),
                         Column('amount', Integer,
                                key='Amount',
                                ),
                         Column('refund_key', Text,
                                key='RefundKey',
                                ),
                         Column('merchant_id', Text,
                                key='MerchantID',
                                ),
                         Column('status', Text,
                                key='Status',
                                ),
                         Column('settlement', Integer,
                                key='Settlement'),
                         Column('error_string', Text,
                                key='ErrorString',
                                ),
                         Column('card_name', Text,
                                key='CardName',
                                ),
                         Column('requested_page', Text,
                                key='RequestedPage',
                                ),
                         Column('card_type', Text,
                                key='CardType',
                                ),
                         Column('mac', Text,
                                key='MAC',
                                ),
                         Column('card_number', Text,
                                key='CardNumber',
                                ),
                         Column('trans_id', Text,
                                key='TransID',
                                ),
                         Column('original_amount', Integer,
                                key='ORIGINAL_AMOUNT',
                                ),
                         Column('surcharge', Integer,
                                key='Surcharge',
                                ),
                         Column('result', Text,
                                key='result',
                                ),
                         Column('ip_address', Text,
                                key='HTTP_X_FORWARDED_FOR',
                                ),

                         Column('creation_timestamp', DateTime,
                                nullable=False,
                                default=func.current_timestamp()),
                         Column('last_modification_timestamp', DateTime,
                                nullable=False,
                                default=func.current_timestamp(),
                                onupdate=func.current_timestamp()),
                         )

voucher_code = Table('voucher_code', metadata,
                Column('id', Integer, primary_key=True),

                Column('code', Text, nullable=False, unique=True),

                Column('type', Text, nullable=False),

                Column('percentage', Integer, nullable=False),

                Column('comment', Text, nullable=False),

                Column('leader_id', Integer,
                       ForeignKey('person.id'),
                       nullable=False,
                       ),

                Column('creation_timestamp', DateTime,
                       nullable=False,
                       default=func.current_timestamp()),
                Column('last_modification_timestamp', DateTime,
                       nullable=False,
                       default=func.current_timestamp(),
                       onupdate=func.current_timestamp()),

                )
