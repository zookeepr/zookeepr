from sqlalchemy import *

person = Table('person',
               Column('id', Integer, primary_key=True),

               Column('email_address', String,
                      nullable=False,
                      unique=True),
                
               Column('password_hash', String),

               # flag that the account has been activated by the user
               # (responded to their confirmation email)
               Column('activated', Boolean,
                      default=False,
                      nullable=False),

               # secondary key, unique identifier within the zookeepr app
               # useful for URLs, not required though (a-la flickr)
               Column('handle', String(40),
                      unique=True,
                      ),
               
               # other personal details
               # the lengths of the fields are chosen arbitrarily
               Column('firstname', String(1024)),
               Column('lastname', String(1024)),
               Column('phone', String(32)),
               Column('fax', String(32)),
                     
               # creation timestamp of the registration
               Column('creation_timestamp', DateTime,
                      nullable=False,
                      key='_creation_timestamp',
                      ),

               # hash of the url generated for easy lookup
               Column('url_hash', String(32),
                      nullable=False,
                      index=True,
                      key='_url_hash',
                      ),
               )

# describe account roles to grant levels of access
role = Table('role',
              Column('id', Integer, primary_key=True),

              # name of role
              Column('name', String,
                     unique=True,
                     nullable=False)
              )

person_role_map = Table('person_role_map',
                        Column('person_id', Integer, ForeignKey('person.id')),
                        Column('role_id', Integer, ForeignKey('role.id'))
                        )
