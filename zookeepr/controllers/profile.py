from zookeepr.lib.base import BaseController
from zookeepr.lib.crud import View
from zookeepr import model

class ProfileController(BaseController, View):
    model = model.Person
    individual = 'profile'
