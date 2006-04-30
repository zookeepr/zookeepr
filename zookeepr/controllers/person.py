from zookeepr.lib.base import *

class PersonController(BaseController):

    def index(self):
        """Show a list of all persons in the system"""
        # GET -> return a list of persons
        # POST -> NO-OP, do GET

        # get persons and assign to the magical template global thing
        c.persons = model.Person.select()
        m.subexec('person/list.myt')

    def view(self, id):
        """View a specific person"""
        # GET -> return person profile
        # POST -> NO-OP

        # assign to the template global
        results = model.Person.select_by(handle=id)
        if len(results) == 0:
            m.abort(404)
        h.log(results[0])
        c.person = results[0]
        m.subexec('person/view.myt')

    def edit(self, id):
        # GET -> return 'edit' form
        # POST -> update with contents of form
        m.write("you're editing person %s" % id)

    def delete(self, id):
        # GET -> return delete approval form
        # POST -> do delete
        m.write("you're deleting person %s" % id)

    def new(self):
        """Create a new person.

        GET requests will return a blank form for submitting all attributes.

        POST requests will create the Person and return a redirect to the
        Person view page.
        """

        errors, defaults = {}, m.request_args
        if request.method == 'POST':
            if defaults:
                # create some object
                p = model.Person(**defaults)
                
                # insert into database
                p.commit()
                
                # redirect somewhere with a thanks message
                return h.redirect_to(action='view', id=defaults['handle'])

        m.subexec('person/new.myt', defaults=defaults, errors=errors)

    def list(self):
        # GET -> retun list of persons?
        # POST -> NO-OP, do same as GET
        m.write("you're getting the list of persons")
