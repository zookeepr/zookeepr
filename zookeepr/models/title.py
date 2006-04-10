from formencode import schema, validators, api
from sqlobject import *

from pylons.database import PackageHub
hub = PackageHub("zookeepr")
__connection__ = hub 

class TitleSchema(schema.Schema):
    def validate(self, input):
        try:
            result = self.to_python(input)
            return result, {}
        except api.Invalid, e:
            return {}, e.unpack_errors()

    title = validators.String(not_empty = True, max = 50)

class Title(SQLObject):
    title = StringCol()

Title.createTable(ifNotExists=True)
