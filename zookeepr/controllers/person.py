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
        c.person = results[0]
        m.subexec('person/view.myt')

    def edit(self, id):
        """Edit a specific person

        GET requests return an 'edit' form, prefilled with the current
        data.

        POST requests update the Person with the data posted.
        """
        # get the Person
        ps = model.Person.select_by(handle=id)
        if len(ps) == 0:
            m.abort(404, 'No such person "%s"' % (id,))
        p = ps[0]

        # initialise variables
        defaults, errors = {}, {}

        # FIXME: gotta be a better way to seed the form
        for k in ['handle', 'email_address', 'firstname', 'lastname', 'phone', 'fax']:
            defaults[k] = getattr(p, k)

        if request.method == 'POST':
            errors, defaults = {}, m.request_args
            if defaults:
                # FIXME: need a better way to reflect form into object
                for (k, v) in defaults.items():
                    setattr(p, k, v)
                p.commit()
                return h.redirect_to(action='index', id=None)

        m.subexec('person/edit.myt', defaults=defaults, errors=errors)

    def delete(self, id):
        """Delete a person.

        GET will return a form asking for approval.

        POST requests with a key 'delete' set to 'ok' will delete the item.

        Invalid ids will return a 404 not found.
        """
        ps = model.Person.select_by(handle=id)
        if len(ps) == 0:
            m.abort(404, "No person '%s' found" % id)

        p = ps[0]
        
        errors, defaults = {}, m.request_args
        if request.method == 'POST':
            if defaults and defaults.has_key('delete') and defaults['delete'] == 'ok':
                p.delete()
                p.commit()

                return h.redirect_to(action='index', id=None)

        m.subexec('person/delete.myt', defaults=defaults, errors=errors)

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
                return h.redirect_to(action='view', id=p.handle)

        m.subexec('person/new.myt', defaults=defaults, errors=errors)

    def list(self):
        # GET -> retun list of persons?
        # POST -> NO-OP, do same as GET
        m.write("you're getting the list of persons")
