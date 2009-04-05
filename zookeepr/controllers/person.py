import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, NotExistingPersonValidator, ExistingPersonValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model import Person, PasswordResetConfirmation

from zookeepr.config.lca_info import lca_info

import datetime

log = logging.getLogger(__name__)



class ForgottenPasswordSchema(BaseSchema):
    email_address = validators.Email(not_empty=True)

    chained_validators = [ExistingPersonValidator()]


class PasswordResetSchema(BaseSchema):
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)

    chained_validators = [validators.FieldsMatch('password', 'password_confirm')]

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

    chained_validators = [NotExistingPersonValidator(), validators.FieldsMatch('password', 'password_confirm')]

class NewPersonSchema(BaseSchema):
    pre_validators = [NestedVariables]

    person = PersonSchema()

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
#    schemas = {'new': NewPersonSchema(),
#               'edit': UpdatePersonSchema()
#              }

#    permissions = {
#                   'roles': [AuthRole('organiser')],
#                   'index': [AuthRole('organiser')],
#                   'signout': [AuthTrue()],
#                   'new': True,
#                   'edit': [AuthFunc('is_same_id'),AuthRole('organiser')],
#                   }


    @authorize(h.auth.is_valid_user)
    def signin(self):
        # Signin is handled by authkit so we just need to redirect stright to home
        if lca_info['conference_status'] == 'open':
            redirect_to(controller='registration', action='status')

        redirect_to('home')

    def signout_confirm(self):
        """ Confirm user wants to sign out
        """
        return render('/person/signout.mako')


    def signout(self):
        """ Sign the user out
            Authikit actually does the work after this finished
        """

        # return home
        redirect_to('home')

    def confirm(self, confirm_hash):
        """Confirm a registration with the given ID.

        `confirm_hash` is a md5 hash of the email address of the registrant, the time
        they regsitered, and a nonce.

        """
        person = Person.find_by_url_hash(confirm_hash)

        if person is None:
            abort(404)

        if person.activated:
            return render('person/already_confirmed.mako')

        person.activated = True

        meta.Session.commit()

        return render('person/confirmed.mako')

    @dispatch_on(POST="_forgotten_password") 
    def forgotten_password(self):
        return render('/person/forgotten_password.mako')

    @validate(schema=ForgottenPasswordSchema(), form='forgotten_password', post_only=False, on_get=True)
    def _forgotten_password(self):
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
        # Check if there is already a password recovery in progress
        reset = PasswordResetConfirmation.find_by_email(self.form_result['email_address'])
        if reset is not None:
            return render('person/in_progress.mako')

        # Ok kick one off
        c.conf_rec = PasswordResetConfirmation(email_address=self.form_result['email_address'])
        meta.Session.add(c.conf_rec)
        meta.Session.commit()

        email(c.conf_rec.email_address, render('person/confirmation_email.mako'))

        return render('person/password_confirmation_sent.mako')

    @dispatch_on(POST="_reset_password") 
    def reset_password(self, url_hash):
        c.conf_rec = PasswordResetConfirmation.find_by_url_hash(url_hash)
        if c.conf_rec is None:
            abort(404)

        return render('person/reset.mako')

    @validate(schema=PasswordResetSchema(), form='reset_password', post_only=False, on_get=True)
    def _reset_password(self, url_hash):
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
        c.conf_rec = PasswordResetConfirmation.find_by_url_hash(url_hash)
        if c.conf_rec is None:
            abort(404)

        now = datetime.datetime.now(c.conf_rec.timestamp.tzinfo)
        if delta > datetime.timedelta(0, 24, 0):
            # this confirmation record has expired
            meta.Session.delete(c.conf_rec)
            meta.Session.commit()
            return render('person/expired.mako')

        person = Person.find_by_email(c.conf_rec.email_address)
        if person is None:
            raise RuntimeError, "Person doesn't exist %s" % c.conf_rec.email_address

        # set the password
        person.password = self.form_result['password']
        # also make sure the person is activated
        person.activated = True

        # delete the conf rec
        meta.Session.delete(c.conf_rec)
        meta.Session.commit()

        return render('person/success.mako')


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


    @authorize(h.auth.is_valid_user)
    def view(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(id), h.auth.has_reviewer_role, h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.registration_status = h.config['app_conf'].get('registration_status')
        c.person = Person.find_by_id(id)

        return render('person/view.mako')

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
