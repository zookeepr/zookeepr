from formencode import schema, validators, api
from sqlobject import *

from pylons.database import PackageHub
hub = PackageHub("zookeepr")
__connection__ = hub 

class PersonSchema(schema.Schema):
    def validate(self, input):
        try:
            result = self.to_python(input)
            return result, {}
        except api.Invalid, e:
            return {}, e.unpack_errors()

    username = validators.String(not_empty = True, max = 50)
    age = validators.Int(not_empty = True)

class Person(SQLObject):
    firstname = StringCol()
    lastname = StringCol()
    title = ForeignKey('title')
    handle = StringCol() # nickname, screenname

    #

    address1 = StringCol()
    address2 = StringCol()
    city = StringCol()
    state = StringCol()
    country = StringCol()
    postcode = StringCol()

    phone = StringCol()
    fax = StringCol()

    email = StringCol()

    #

    homepage = StringCol()
    company = StringCol()
    companyurl = StringCol()
    bio = StringCol()

Person.createTable(ifNotExists=True)
