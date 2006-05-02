from zookeepr.lib.base import *

class CfpController(BaseController):
    """Controller for submitting something to the conference"""
    def index(self):
        return h.redirect_to(action='new')

    def view(self, id):
        """View a submission."""
        m.write("you're viewing submission %s" % id)

    def new(self):
        """Create a new submission"""
        new_person = model.Person()
        new_submission = model.Submission()

        if request.method == 'POST':
            new_person.update(**m.request_args['person'])
            new_submission.update(**m.request_args['submission'])
            new_submission.person = new_person

            if new_person.validate() and new_submission.validate():
                # save to database
                objectstore.flush()
                return h.redirect_to(controller='person', action='view', id=new_person.handle)

        c.submissiontypes = model.SubmissionType.select()
        c.person = new_person
        setattr(c, 'submission', new_submission)
        m.subexec('cfp/new.myt')

    def edit(self, id):
        """Edit a submission."""
        m.write("you're editing submission %s" % id)

    def remove(self, id):
        """Remove a submission"""
        m.write("you're removing submission %s" % id)
