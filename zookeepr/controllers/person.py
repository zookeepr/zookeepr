from zookeepr.lib.base import *

class PersonController(BaseController):

    def index(self):
        # so the default action for a person is to view your own
        # person, right?
        m.write("person index")

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

        errors, defaults = {}, m.request_args
        if defaults:
            # create some object
            # insert into database
            # redirect somewhere with a thanks message
            return h.redirect_to(action='view', id=defaults['handle'])
        m.subexec('person/new.myt', defaults=defaults, errors=errors)

    def list(self):
        # GET -> retun list of persons?
        # POST -> NO-OP, do same as GET
        m.write("you're getting the list of persons")
