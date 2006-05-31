from zookeepr.lib.base import *

class CfpController(BaseController):
    """Controller for submitting something to the conference"""
    def index(self):
        """Create a new submission"""

        session = create_session()
        
        new_person = model.Person()
        new_submission = model.Submission()

        if request.method == 'POST':
            for k in m.request_args['person']:
                setattr(new_person, k, m.request_args['person'][k].value)
            for k in m.request_args['submission']:
                setattr(new_person, k, m.request_args['submission'][k].value)
            new_submission.person = new_person

            if True: #new_person.validate() and new_submission.validate():
                # save to database
                session.save(new_person)
                session.save(new_submission)
                session.flush()
                session.close()
                
                return h.redirect_to(controller='person', action='view', id=new_person.handle)
            else:
                session.clear()

        # set up for the cfp form
        c.submissiontypes = session.query(model.SubmissionType).select()
        c.person = new_person
        setattr(c, 'submission', new_submission)
        m.subexec('cfp/new.myt')
