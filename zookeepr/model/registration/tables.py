import sqlalchemy.mods.threadlocal
from sqlalchemy import *

registration = Table('registration',
                     Column('id', Integer, primary_key=True),

                     Column('account_id', Integer, ForeignKey('account.id'))
                     )
