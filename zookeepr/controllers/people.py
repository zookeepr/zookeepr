from zookeepr.lib.base import *

class PeopleController(BaseController):
    def index(self):
        # so the default actoin for a person is to view your own person, right?
        pass

    def view(self, id):
        m.write("you're viewing person %s" % id)

    def edit(self, id):
        m.write("you're editing person %s" % id)

    def delete(self, id):
        m.write("you're deleting person %s" % id)

    def 
