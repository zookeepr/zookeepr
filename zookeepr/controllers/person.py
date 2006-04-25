from zookeepr.lib.base import *

class PersonController(BaseController):
    def index(self):
        # so the default action for a person is to view your own
        # person, right?
        m.write("people index")

    def view(self, id):
        # GET -> return person profile
        # POST -> NO-OP
        m.write("you're viewing person %s" % id)

    def edit(self, id):
        # GET -> return 'edit' form
        # POST -> update with contents of form
        m.write("you're editing person %s" % id)

    def delete(self, id):
        # GET -> return delete approval form
        # POST -> do delete
        m.write("you're deleting person %s" % id)

    def new(self):
        # GET -> get 'new' form
        # POST -> create new
        m.write("you're creating a person")
