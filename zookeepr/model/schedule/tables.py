from sqlalchemy import *

from zookeepr.model import metadata

# Stores conference stream names
stream = Table('stream', metadata,
               Column('id', Integer, primary_key=True),

               Column('name', String,
                      nullable=False,
                      unique=True,
                      ),
               )
