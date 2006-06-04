import types
from formencode import validators, compound, schema, variabledecode
from zookeepr.lib.base import *

class PersonValidator(schema.Schema):
    handle = validators.PlainText()
    password = validators.PlainText()
    password_confirm = validators.PlainText()    
    email_address = validators.Email()

class SubmissionValidator(schema.Schema):
    title = validators.PlainText()
    url = validators.URL()
    abstract = validators.PlainText()
    attachment = compound.Any(
        validators.ConfirmType(type=types.FileType),
        validators.String())

class CfpValidator(schema.Schema):
    person = PersonValidator()
    submission = SubmissionValidator()
    commit = validators.String()
    pre_validators = [variabledecode.NestedVariables]

class CfpController(BaseController):
    """Controller for submitting something to the conference"""
    validator = {"index" : CfpValidator()}
    
    def index(self):
        """Create a new submission"""

        session = create_session()
        
        new_person = model.Person()
        new_submission = model.Submission()

        if request.method == 'POST':
            for k in m.request_args['person']:
                if hasattr(m.request_args['person'][k], 'value'):
                    v = m.request_args['person'][k].value
                else:
                    v = m.request_args['person'][k]
                setattr(new_person, k, v)
                
            for k in m.request_args['submission']:
                if hasattr(m.request_args['submission'][k], 'value'):
                    v = m.request_args['submission'][k].value
                else:
                    v = m.request_args['submission'][k]
                setattr(new_submission, k, v)
                
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
