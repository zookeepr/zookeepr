from zookeepr.lib.base import *

class SubmissiontypeController(BaseController):
    
    def index(self):
        """Show a list of all submission types currently in the system."""
        # GET -> return list of subtypes
        # POST -> NOOP, do GET

        # get submission types and assign to the magical template global
        c.submissiontypes = model.SubmissionType.select()
        m.subexec('submissiontype/list.myt')

    def view(self, id):
        """View a specific submission type."""
        # GET -> return subtype
        # POST -> NOOP, do GET

        # assign to the template global
        c.submissiontype = model.SubmissionType.get(id)
        m.subexec('submissiontype/view.myt')

    def edit(self, id):
        """Allow editing of a specific submission type.

        GET requests return an 'edit' form, prefilled with the current
        data.

        POST requests update the SubmissionType with the data posted.
        """
        # get us this SubType
        st = model.SubmissionType.get(id)
        # initialise variables
        defaults, errors = {}, {}
        
        # FIXME: gotta be a better way to seed the form
        for k in ['name']:
            defaults[k] = getattr(st, k)
            
        if request.method == 'POST':
            errors, defaults = {}, m.request_args
            if defaults:
                # FIXME: is there a better way to reflect form data into object
                for (k, v) in defaults.items():
                    setattr(st, k, v)
                st.commit()
                return h.redirect_to(action='index', id=None)

        m.subexec('submissiontype/edit.myt', defaults=defaults, errors=errors)

    def delete(self, id):
        """Delete a submission type.

        GET will return a form asking for approval.

        POST requests with a key 'delete' set to 'ok' will delete the item.

        Invalid ids will return a 404 not found.
        """
        errors, defaults = {}, m.request_args
        
        #h.log(defaults)
        if defaults:
            #h.log(defaults)
            st = model.SubmissionType.get(id)
            h.log(st)
            st.delete()
            st.commit()
            return h.redirect_to(action='index', id=None)
        m.subexec('submissiontype/delete.myt', defaults=defaults, errors=errors)

    def new(self):
        """Create a new submission type.

        GET requests will return a blank form for submitting all attributes.

        POST requests will create the submission type, and return a redirect
        to view the new SubType.
        """
        errors, defaults = {}, m.request_args
        if defaults:
            # create, etc
            st = model.SubmissionType(**defaults)

            # put in db
            st.commit()

            # redirect to.. somewhere
            return h.redirect_to(action='view', id=st.id)
        
        m.subexec('submissiontype/new.myt', defaults=defaults, errors=errors)
