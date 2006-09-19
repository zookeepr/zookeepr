import sqlalchemy.mods.threadlocal
from sqlalchemy import *

# Stores conference stream names
stream = Table('stream',
               Column('id', Integer, primary_key=True),

               Column('name', String,
                      nullable=False,
                      unique=True,
                      ),
               )
