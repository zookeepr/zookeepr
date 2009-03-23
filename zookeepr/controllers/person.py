import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema # FIXME, NotExistingPersonValidator

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model.person import Person #, PasswordResetConfirmation

log = logging.getLogger(__name__)



#import datetime
#
#from formencode.schema import Schema
#import sqlalchemy
#
#from zookeepr.lib.auth import PersonAuthenticator, retcode
#from zookeepr.lib.base import *
#from zookeepr.model import Person, PasswordResetConfirmation
#
#from zookeepr.lib.base import *
#from zookeepr.lib.crud import Read, Update, List
#from zookeepr.lib.auth import SecureController, AuthRole, AuthFunc, AuthTrue
#from zookeepr import model
#from zookeepr.model.core.domain import Role
#from zookeepr.model.core.tables import person_role_map
#from sqlalchemy import and_
#from zookeepr.config.lca_info import lca_info

# TODO : formencode.Invalid support HTML for email markup... - Josh H 07/06/08
# TODO : Validate not_empty nicer... needs to co-exist better with actual validators and also place a message up the top - Josh H 07/06/08
# TODO : Proper email validation? I thought it existed but it doesn't seem like it. Should be easy to add in, just too late to mess with this year - Josh H 05/09/08

class AuthenticationValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        l = PersonAuthenticator()
        r = l.authenticate(value['email_address'], value['password'])
        if r == retcode.SUCCESS:
            pass
        elif r == retcode.FAILURE:
            raise Invalid("""Your sign-in details are incorrect; try the
                'Forgotten your password' link below or sign up for a new
                person.""", value, state)
        elif r == retcode.TRY_AGAIN: # I don't think this occurs - Josh H 06/06/08
            raise Invalid('A problem occurred during sign in; please try again later or contact <a href="mailto:' + lca_info['contact_email'] + '">' + lca_info['contact_email'] + '</a>.', value, state)
        elif r == retcode.INACTIVE:
            raise Invalid("You haven't yet confirmed your registration, please refer to your email for instructions on how to do so.", value, state)
        else:
            raise RuntimeError, "Unhandled authentication return code: '%r'" % r


#class ExistingPersonValidator(validators.FancyValidator):
#    def validate_python(self, value, state):
#        persons = state.query(Person).filter_by(email_address=value['email_address']).first()
#        if persons == None:
#            raise Invalid('Your supplied e-mail does not exist in our database. Please try again or if you continue to have problems, contact %s.' % lca_info['contact_email'], value, state)


class LoginValidator(BaseSchema):
    email_address = validators.Email(not_empty=True)
    password = validators.String(not_empty=True)

    chained_validators = [AuthenticationValidator()]


#class ForgottenPasswordSchema(BaseSchema):
#    email_address = validators.String(not_empty=True)
#    chained_validators = [ExistingPersonValidator()]


#class PasswordResetSchema(BaseSchema):
#    password = validators.String(not_empty=True)
#    password_confirm = validators.String(not_empty=True)
#
#    chained_validators = [validators.FieldsMatch('password', 'password_confirm')]

class PersonSchema(BaseSchema):

    firstname = validators.String(not_empty=True)
    lastname = validators.String(not_empty=True)
    company = validators.String()
    email_address = validators.Email(not_empty=True)
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)
    phone = validators.String()
    mobile = validators.String()
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    postcode = validators.String(not_empty=True)
    country = validators.String(not_empty=True)

    # FIXME chained_validators = [NotExistingPersonValidator(), validators.FieldsMatch('password', 'password_confirm')]
    chained_validators = [validators.FieldsMatch('password', 'password_confirm')]

class NewPersonSchema(BaseSchema):
    person = PersonSchema()
    pre_validators = [NestedVariables]

#class _UpdatePersonSchema(BaseSchema):
#    # Redefine the schema to remove email and password validation
#    # FIXME: We can't change the Schema's drastically at this point. This edit schema needs a review
#    firstname = validators.String(not_empty=True)
#    lastname = validators.String(not_empty=True)
#    company = validators.String()
#    phone = validators.String()
#    mobile = validators.String()
#    address1 = validators.String(not_empty=True)
#    address2 = validators.String()
#    city = validators.String(not_empty=True)
#    state = validators.String()
#    postcode = validators.String(not_empty=True)
#    country = validators.String(not_empty=True)
#
#    pre_validators = []
#    chained_validators = []

#class UpdatePersonSchema(BaseSchema):
#    # Redefine the schema to remove email and password validation
#    # FIXME: We can't change the Schema's drastically at this point. This edit schema needs a review
#    person = _UpdatePersonSchema()
#    pre_validators = [NestedVariables]

class PersonController(BaseController): #SecureController, Read, Update, List):
#    model = model.Person
#    individual = 'person'

#    schemas = {'new': NewPersonSchema(),
#               'edit': UpdatePersonSchema()
#              }

#    permissions = {'view': [AuthFunc('is_same_id'), AuthRole('organiser'), AuthRole('reviewer')],
#                   'roles': [AuthRole('organiser')],
#                   'index': [AuthRole('organiser')],
#                   'signin': True,
#                   'signout': [AuthTrue()],
#                   'new': True,
#                   'edit': [AuthFunc('is_same_id'),AuthRole('organiser')],
#                   'forgotten_password': True,
#                   'reset_password': True,
#                   'confirm': True
#                   }


    @authorize(ValidAuthKitUser())
    def test(self):
        return "You are authenticated!"

    @dispatch_on(POST="_signin") 
    def signin(self):

        # Save the URL we came from for auth, might not be needed if we move to authkit
        if 'url' in request.GET:
            session['sign_in_redirect'] = '/' + request.GET['url']
            session.save()

        if c.signed_in_person:
            return render('person/already_loggedin.mako')

        return render('person/signin.mako')

    @validate(schema=LoginValidator(), form='new', post_only=False, on_get=True, variable_decode=True)
    def _signin(self):
# do the authorisation here or in validator?
                # get person
                # check auth
                # set session cookies
                person = self.dbsession.query(Person).filter_by(email_address=result['email_address']).one()
                if person:
                    # at least one Person matches, save it
                    session['signed_in_person_id'] = person.id
                    session.save()

                    # Redirect to original URL if it exists
                    if 'sign_in_redirect' in session:
                        redirect_to(str(session['sign_in_redirect']))

                    # return to the registration status
                    # (while registrations are open)
                    if lca_info['conference_status'] == 'open':
                        redirect_to(controller='registration', action='status')

                    # return home
                    redirect_to('home')

    def signout_confirm(self):
        """ Confirm user wants to sign out
        """
        return render('/person/signout.mako')


    def signout(self):
        """ Sign the user out
            Authikit actually does the work after this finished
        """
        # FIXME DO we delete the session? Authkit has it's own
        # delete and invalidate the session
        #session.delete()
        #session.invalidate()

        # return home
        redirect_to('home')

    def confirm(self, confirm_hash):
        """Confirm a registration with the given ID.

        `confirm_hash` is a md5 hash of the email address of the registrant, the time
        they regsitered, and a nonce.

        """
        r = self.dbsession.query(Person).filter_by(url_hash=confirm_hash).first()

        if r is None:
            abort(404)

        r.activated = True

        self.dbsession.update(r)
        self.dbsession.flush()

        return render_response('person/confirmed.myt')

    def forgotten_password(self):
        """Action to let the user request a password change.

        GET returns a form for emailing them the password change
        confirmation.

        POST checks the form and then creates a confirmation record:
        date, email_address, and a url_hash that is a hash of a
        combination of date, email_address, and a random nonce.

        The email address must exist in the person database.

        The second half of the password change operation happens in
        the ``confirm`` action.
        """
        defaults = dict(request.POST)
        errors = {}

        if defaults:
            result, errors = ForgottenPasswordSchema().validate(defaults, self.dbsession)

            if not errors:
                c.conf_rec = PasswordResetConfirmation(result['email_address'])
                self.dbsession.save(c.conf_rec)
                try:
                    self.dbsession.flush()
                except sqlalchemy.exceptions.SQLError, e:
                    self.dbsession.clear()
                    # FIXME exposes sqlalchemy!
                    return render_response('person/in_progress.myt')

                email(c.conf_rec.email_address,
                    render('person/confirmation_email.myt', fragment=True))
                return render_response('person/password_confirmation_sent.myt')
        return render_response('person/forgotten_password.myt', defaults=defaults, errors=errors)


    def reset_password(self, url_hash):
        """Confirm a password change request, and let the user change
        their password.

        `url_hash` is a hash of the email address, with which we can
        look up the confuirmation record in the database.

        If `url_hash` doesn't exist, 404.

        If `url_hash` exists and the date is older than 24 hours,
        warn the user, offer to send a new confirmation, and delete the
        confirmation record.

        GET returns a form for setting their password, with their email
        address already shown.

        POST checks that the email address (in the session, not in the
        form) is part of a valid person record (again).  If the record
        exists, then update the password, hashed.  Report success to the
        user.  Delete the confirmation record.

        If the record doesn't exist, throw an error, delete the
        confirmation record.
        """
        crecs = self.dbsession.query(PasswordResetConfirmation).filter_by(url_hash=url_hash).all()
        if len(crecs) == 0:
            abort(404)

        c.conf_rec = crecs[0]

        now = datetime.datetime.now(c.conf_rec.timestamp.tzinfo)
        delta = now - c.conf_rec.timestamp
        if delta > datetime.timedelta(24, 0, 0):
            # this confirmation record has expired
            self.dbsession.delete(c.conf_rec)
            self.dbsession.flush()
            return render_response('person/expired.myt')

        # now process the form
        defaults = dict(request.POST)
        errors = {}

        if defaults:
            result, errors = PasswordResetSchema().validate(defaults, self.dbsession)

            if not errors:
                persons = self.dbsession.query(Person).filter_by(email_address=c.conf_rec.email_address).all()
                if len(persons) == 0:
                    raise RuntimeError, "Person doesn't exist %s" % c.conf_rec.email_address

                # set the password
                persons[0].password = result['password']
                # also make sure the person is activated
                persons[0].activated = True

                # delete the conf rec
                self.dbsession.delete(c.conf_rec)
                self.dbsession.flush()

                return render_response('person/success.myt')

        # FIXME: test the process above
        return render_response('person/reset.myt', defaults=defaults, errors=errors)

    def edit(self):
        """UPDATE PERSON"""
        defaults = dict(request.POST)
        errors = {}

        if defaults:
            result, errors = UpdatePersonSchema().validate(defaults, self.dbsession)

            if not errors:
                # update the objects with the validated form data
                for k in result['person']:
                    setattr(self.obj, k, result['person'][k])
                self.dbsession.update(self.obj)
                self.dbsession.flush()

                default_redirect = dict(action='view', id=self.identifier(self.obj))
                self.redirect_to('edit', default_redirect)

        return render_response('person/edit.myt',
                               defaults=defaults, errors=errors)


    @dispatch_on(POST="_new") 
    def new(self):
        """Create a new person form.

        Non-CFP persons get created through this interface.

        See ``cfp.py`` for more person creation code.
        """
        if c.signed_in_person:
            return render('/person/already_loggedin.mako')

        defaults = {
            'person.country': 'AUSTRALIA'
        }
        form = render('/person/new.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=NewPersonSchema(), form='new', post_only=False, on_get=True, variable_decode=True)
    def _new(self):
        """Create a new person submit.
        """

        # Remove fields not in class
        results = self.form_result['person']
        del results['password_confirm']
        c.person = Person(**results)
        meta.Session.add(c.person)
        meta.Session.commit()

        email(c.person.email_address, render('/person/new_person_email.mako'))

        return render('/person/thankyou.mako')



    def index(self):
        r = AuthRole('organiser')
        if self.logged_in():
            if not r.authorise(self):
                redirect_to(action='view', id=session['signed_in_person_id'])
        else:
            abort(403)

        return super(PersonController, self).index()

    def _can_edit(self):
        try:
            permission = (self.obj.id == session['signed_in_person_id']) or AuthRole('organiser')
        except AttributeError:
            #FIXME: ugly work around for when an individual person object isn't loaded.
            # This method is meant to be used to display the "edit" link when an organiser or the owner views a person's profile.
            # However, the index method in the CRUD middleware also uses the _can_edit definition so we have this ugly workaround.
            permission = False
        return permission

    def view(self):
        c.registration_status = request.environ['paste.config']['app_conf'].get('registration_status')
        if self.logged_in():
            roles = self.dbsession.query(Role).all()
            for role in roles:
                r = AuthRole(role.name)
                if r.authorise(self):
                    setattr(c, 'is_%s_role' % role.name, True)

        return super(PersonController, self).view()

    def roles(self):
        """ Lists and changes the person's roles. """

        td = '<td valign="middle">'
        res = ''
        res += '<p><b>'+self.obj.firstname+' '+self.obj.lastname+'</b></p><br>'
        data = dict(request.POST)
        if data:
          role = int(data['role'])
          act = data['Commit']
          if act not in ['Grant', 'Revoke']: raise "foo!"
          r = self.dbsession.query(Role).filter_by(id=role).one()
          res += '<p>' + act + ' ' + r.name + '.'
          if act=='Revoke':
            person_role_map.delete(and_(
              person_role_map.c.person_id == self.obj.id,
              person_role_map.c.role_id == role)).execute()
          if act=='Grant':
            person_role_map.insert().execute(person_id = self.obj.id,
                                                            role_id = role)


        res += '<table>'
        for r in self.dbsession.query(Role).all():
          res += '<tr>'
          # can't use AuthRole here, because it may be out of date
          has = len(person_role_map.select(whereclause =
            and_(person_role_map.c.person_id == self.obj.id,
              person_role_map.c.role_id == r.id)).execute().fetchall())

          if has>1:
            # this can happen if two people Grant at once, or one person
            # does a Grant and reloads/reposts.
            res += td + 'is %d times' % has
            has = 1
          else:
            res += td+('is not', 'is')[has]
          res += td+r.name

          res += td+h.form(h.url())
          res += h.hidden_field('role', r.id)
          res += h.submitbutton(('Grant', 'Revoke')[has])
          res += h.end_form()

        res += '</table>'

        c.res = res

        return render_response('person/roles.myt')

    def is_same_id(self, *args):
        return self.obj.id == session['signed_in_person_id']
