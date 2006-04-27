from zookeepr.lib.base import *

class SubmissiontypeController(BaseController):
    
    def index(self):
        # index action lists
        # GET -> return list of subtypes
        # POST -> NOOP, do GET

        # get submission types and assign to thingy
        c.submissiontypes = model.SubmissionType.mapper.select(model.submission_type.c.id>=0)
        
        m.subexec('submissiontype/list.myt')

    def view(self, id):
        # GET -> return subtype
        # POST -> NOOP, do GET

        # assign to the template global
        c.submissiontype = model.SubmissionType.get(id)

        # call the template
        m.subexec('submissiontype/view.myt')

    def edit(self, id):
        # GET -> return 'edit' form
        # POST -> update entry with form results
        st = model.SubmissionType.get(id)
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
        # GET -> return 'delete' formm
        # POST -> act on results of delete form
        errors, defaults = {}, m.request_args
        #h.log(defaults)
        if defaults:
            #h.log(defaults)
            st = model.SubmissionType.get(id)
            st.delete()
            st.commit()
            return h.redirect_to(action='index', id=None)
        m.subexec('submissiontype/delete.myt', defaults=defaults, errors=errors)

    def new(self):
        # GET -> return 'new' form
        # POST -> create new with results of form
        errors, defaults = {}, m.request_args
        if defaults:
            # create, etc
            st = model.SubmissionType(**defaults)

            # put in db
            st.commit()

            # redirect to.. somewhere
            return h.redirect_to(action='view', id=st.id)
        
        m.subexec('submissiontype/new.myt', defaults=defaults, errors=errors)
