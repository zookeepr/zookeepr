import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, NotExistingPersonValidator, ExistingPersonValidator, PersonSchema
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model import Person, PasswordResetConfirmation, Role

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

class NewPersonSchema(BaseSchema):
    pre_validators = [NestedVariables]

    person = PersonSchema()

class _UpdatePersonSchema(BaseSchema):
    firstname = validators.String(not_empty=True)
    lastname = validators.String(not_empty=True)
    company = validators.String()
    phone = validators.String()
    mobile = validators.String()
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    postcode = validators.String(not_empty=True)
    country = validators.String(not_empty=True)

class UpdatePersonSchema(BaseSchema):
    person = _UpdatePersonSchema()
    pre_validators = [NestedVariables]

class RoleSchema(BaseSchema):
    role = validators.String(not_empty=True)
    action = validators.OneOf(['Grant', 'Revoke'])

class PersonController(BaseController): #Read, Update, List
    @authorize(h.auth.is_valid_user)
    def signin(self):
        # Signin is handled by authkit so we just need to redirect stright to home

        h.flash('You have signed in')

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
        h.flash('You have signed out')
        redirect_to('home')

    def confirm(self, confirm_hash):
        """Confirm a registration with the given ID.

        `confirm_hash` is a md5 hash of the email address of the registrant, the time
        they regsitered, and a nonce.

        """
        person = Person.find_by_url_hash(confirm_hash)

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

    @authorize(h.auth.is_valid_user)
    @dispatch_on(POST="_edit") 
    def edit(self, id):
        c.form = 'edit'
        c.person = Person.find_by_id(id)

        defaults = h.object_to_defaults(c.person, 'person')

        form = render('/person/edit.mako')
        return htmlfill.render(form, defaults)


    @authorize(h.auth.is_valid_user)
    @validate(schema=UpdatePersonSchema(), form='edit', post_only=False, on_get=True, variable_decode=True)
    def _edit(self, id):
        """UPDATE PERSON"""
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.person = Person.find_by_id(id)

        for key in self.form_result['person']:
            setattr(c.person, key, self.form_result['person'][key])

        # update the objects with the validated form data
        meta.Session.commit()

        redirect_to(action='view', id=id)


    @dispatch_on(POST="_new") 
    def new(self):
        """Create a new person form.

        Non-CFP persons get created through this interface.

        See ``cfp.py`` for more person creation code.
        """
        if h.signed_in_person():
            h.flash("You're already logged in")
            redirect_to('home')

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

    @authorize(h.auth.has_organiser_role)
    def index(self):
        c.person_collection = Person.find_all()
        return render('/person/list.mako')

    @authorize(h.auth.is_valid_user)
    def view(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(id), h.auth.has_reviewer_role, h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.registration_status = h.config['app_conf'].get('registration_status')
        c.person = Person.find_by_id(id)

        return render('person/view.mako')

    @dispatch_on(POST="_roles") 
    @authorize(h.auth.has_organiser_role)
    def roles(self, id):

        c.person = Person.find_by_id(id)
        c.roles = Role.find_all()
        return render('person/roles.mako')


    @authorize(h.auth.has_organiser_role)
    @validate(schema=RoleSchema, form='roles', post_only=False, on_get=True)
    def _roles(self, id):
        """ Lists and changes the person's roles. """

        c.person = Person.find_by_id(id)
        c.roles = Role.find_all()

        role = self.form_result['role']
        action = self.form_result['action']

        role = Role.find_by_name(name=role)

        if action == 'Revoke':
            c.person.roles.remove(role)
        elif action == 'Grant':
            c.person.roles.append(role)

        meta.Session.commit()

        h.flash(action + ' ' + role.name)

        return render('person/roles.mako')
