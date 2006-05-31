from zookeepr.lib.base import *

class CfpController(BaseController):
    """Controller for submitting something to the conference"""
    def index(self):
        """Create a new submission"""

        session = create_session()
        
        new_person = model.Person()
        new_submission = model.Submission()

        if request.method == 'POST':
            new_person.update(**m.request_args['person'])
            new_submission.update(**m.request_args['submission'])
            new_submission.person = new_person

            if new_person.validate() and new_submission.validate():
                # save to database
                session.save()
                session.flush()
                return h.redirect_to(controller='person', action='view', id=new_person.handle)
            else:
                session.clear()

        # set up for the cfp form
        c.submissiontypes = session.query(model.SubmissionType).select()
        c.person = new_person
        setattr(c, 'submission', new_submission)
        m.subexec('cfp/new.myt')
