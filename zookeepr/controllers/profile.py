from zookeepr.lib.base import *
from zookeepr.lib.crud import View
from zookeepr import model

class ProfileController(BaseController, View):
    model = model.Person
    individual = 'profile'
