## NOTE
##   If you plan on using SQLObject, the following should be un-commented and provides
##   a starting point for setting up your schema

#from sqlobject import *
#from pylons.database import PackageHub
#hub = PackageHub("zookeepr")
#__connection__ = hub

# You should then import your SQLObject classes
# from myclass import MyDataClass

from userinfo import UserInfo, UserInfoSchema
from person import Person, PersonSchema
