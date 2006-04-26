from zookeepr.lib.base import *

class SubmissiontypeController(BaseController):
    def index(self):
        pass

    def view(self, id):
        # GET -> return subtype
        # POST -> NOOP, do GET
        m.write('view subtype %s' % id)

    def edit(self, id):
        # GET -> return 'edit' form
        # POST -> update entry with form results
        m.write('edit subtype %s' % id)

    def delete(self, id):
        # GET -> return 'delete' formm
        # POST -> act on results of delete form
        errors, defaults = {}, m.request_args
        if defaults:
            return h.redirect_to(action='list', id=None)
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

    def list(self):
        # GET -> return list of subtypes
        # POST -> NOOP, do GET
        m.write('list subtypes')
