from zookeepr.lib.base import *

class PersonController(BaseController, View, Modify):
    model = model.Person
    individual = 'person'
    key = 'handle'
