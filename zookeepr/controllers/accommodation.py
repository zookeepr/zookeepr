from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.base import *
from zookeepr.lib.crud import List

class AccommodationController(SecureController, List):
    individual = 'accommodation'
    model = model.Accommodation
    permissions = {'index': [AuthRole('site-admin')],
                   }
