# from formencode import schema, validators, api
# from sqlobject import *

# from pylons.database import PackageHub
# hub = PackageHub("zookeepr")
# __connection__ = hub 

# class UserInfoSchema(schema.Schema):
#     def validate(self, input):
#         try:
#             result = self.to_python(input)
#             return result, {}
#         except api.Invalid, e:
#             return {}, e.unpack_errors()

#     username = validators.String(not_empty = True, max = 50)
#     age = validators.Int(not_empty = True)

# class UserInfo(SQLObject):
#     username = StringCol()
#     age = IntCol()

# UserInfo.createTable(ifNotExists=True)
