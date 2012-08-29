import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema, NotExistingPersonValidator, ExistingPersonValidator, PersonSchema, IAgreeValidator, SameEmailAddress, CountryValidator
import zkpylons.lib.helpers as h
from zkpylons.lib.helpers import check_for_incomplete_profile

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import Person, PasswordResetConfirmation, Role
from zkpylons.model import ProposalStatus
from zkpylons.model import SocialNetwork
from zkpylons.model import Travel

from zkpylons.config.lca_info import lca_info, lca_rego

from zkpylons.lib.ssl_requirement import enforce_ssl

import datetime
import json
import urllib
import urllib2

log = logging.getLogger(__name__)



class ForgottenPasswordSchema(BaseSchema):
    email_address = validators.Email(not_empty=True)

class PasswordResetSchema(BaseSchema):
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)

    chained_validators = [validators.FieldsMatch('password', 'password_confirm')]

class _SocialNetworkSchema(BaseSchema):
   name = validators.String()
   account_name = validators.String()

class IncompletePersonSchema(BaseSchema):
    email_address = validators.Email(not_empty=True)
    email_address2 = validators.Email(not_empty=True)
    chained_validators = [NotExistingPersonValidator(), SameEmailAddress()]

class NewIncompletePersonSchema(BaseSchema):
    pre_validators = [NestedVariables]
    person = IncompletePersonSchema()

class NewPersonSchema(BaseSchema):
    pre_validators = [NestedVariables]

    person = PersonSchema()
    social_network = ForEach(_SocialNetworkSchema())

class _UpdatePersonSchema(BaseSchema):
    firstname = validators.String(not_empty=True)
    lastname = validators.String(not_empty=True)
    email_address = validators.Email(not_empty=True)
    company = validators.String()
    phone = validators.String()
    mobile = validators.String()
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    postcode = validators.String(not_empty=True)
    country = CountryValidator(not_empty=True)
    i_agree = validators.Bool(if_missing=False)

    chained_validators = [IAgreeValidator("i_agree")]

class UpdatePersonSchema(BaseSchema):
    person = _UpdatePersonSchema()
    social_network = ForEach(_SocialNetworkSchema())
    pre_validators = [NestedVariables]

class AuthPersonValidator(validators.FancyValidator):
    def validate_python(self, values, state):
        c.email = values['email_address']
        c.person = Person.find_by_email(c.email)
        error_message = None
        if c.person is None:
            error_message = "Your sign-in details are incorrect; try the 'Forgotten your password' link below or sign up for a new person."
        elif not c.person.activated:
            error_message = "You haven't yet confirmed your registration, please refer to your email for instructions on how to do so."
        elif not c.person.check_password(values['password']):
            error_message = "Your sign-in details are incorrect; try the 'Forgotten your password' link below or sign up for a new person."
        if error_message:
            message = "Login failed"
            error_dict = {'email_address': error_message}
            raise Invalid(message, values, state, error_dict=error_dict)

class PersonaValidator(validators.FancyValidator):
    def validate_python(self, values, state):
        assertion = values['assertion']
        audience = h.url_for(qualified=True, controller='home').strip("/")

        page = urllib2.urlopen('https://verifier.login.persona.org/verify',
                               urllib.urlencode({ "assertion": assertion,
                                                  "audience": audience}))
        data = json.load(page)
        if data['status'] == 'okay':
            c.email = data['email']
            c.person = Person.find_by_email(c.email)

        if c.person is None:
            if not lca_info['account_creation']:
                error_message = "Your sign-in details are incorrect; try the 'Forgotten your password' link below."
                message = "Login failed"
                error_dict = {'email_address': error_message}
                raise Invalid(message, values, state, error_dict=error_dict)

            # Create a new account for this email address
            c.person = Person()
            c.person.email_address = data['email']
            c.person.activated = True
            meta.Session.add(c.person)
            meta.Session.commit()

        if not c.person.activated:
            # Persona returns verified emails only, so might as well confirm this one...
            c.person.activated = True
            meta.Session.commit()


class LoginPersonSchema(BaseSchema):
    email_address = validators.Email(not_empty=True)
    password = validators.String(not_empty=True)
    chained_validators = [AuthPersonValidator()]

class LoginSchema(BaseSchema):
    person = LoginPersonSchema()
    pre_validators = [NestedVariables]

class PersonaLoginSchema(BaseSchema):
    assertion = validators.String(not_empty=True)
    chained_validators = [PersonaValidator()]

class RoleSchema(BaseSchema):
    role = validators.String(not_empty=True)
    action = validators.OneOf(['Grant', 'Revoke'])

class TravelSchema(BaseSchema):
    origin_airport = validators.String(not_empty=True)
    destination_airport = validators.String(not_empty=True)
    pre_validators = [NestedVariables]

class OfferSchema(BaseSchema):
    status = validators.OneOf(['accept', 'withdraw', 'contact'])
    travel = TravelSchema(if_missing=None)
    pre_validators = [NestedVariables]

class PersonController(BaseController): #Read, Update, List
    @enforce_ssl(required_all=True)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_signin")
    def signin(self):

        role_error = session.pop('role_error', None)
        if role_error:
            h.flash(role_error)
        elif h.signed_in_person():
            h.flash("You're already logged in")
            redirect_to('home')

        return render('/person/signin.mako')

    def finish_login(self, email):
        # Tell authkit we authenticated them
        request.environ['paste.auth_tkt.set_user'](email)

        h.check_for_incomplete_profile(c.person)

        h.flash('You have signed in')

        redirect_location = session.pop('redirect_to', None)
        if redirect_location:
            redirect_to(str(redirect_location))

        if lca_info['conference_status'] == 'open':
            redirect_to(controller='registration', action='status')

        redirect_to('home')

    @validate(schema=LoginSchema(), form='signin', post_only=True, on_get=False, variable_decode=True)
    def _signin(self):
        self.finish_login(c.email)

    @validate(schema=PersonaLoginSchema(), form='persona_login', post_only=True, on_get=False, variable_decode=True)
    def persona_login(self):
        self.finish_login(c.email)

    def signout_confirm(self, id=None):
        """ Confirm user wants to sign out
        """
        if id is not None:
            redirect_to(action='signout_confirm', id=None)

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

    @validate(schema=ForgottenPasswordSchema(), form='forgotten_password', post_only=True, on_get=True, variable_decode=True)
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
        c.email = self.form_result['email_address']
        c.person = Person.find_by_email(c.email)

        if c.person is not None:
            # Check if there is already a password recovery in progress
            reset = PasswordResetConfirmation.find_by_email(c.email)
            if reset is not None:
                return render('person/in_progress.mako')

            # Ok kick one off
            c.conf_rec = PasswordResetConfirmation(email_address=c.email)
            meta.Session.add(c.conf_rec)
            meta.Session.commit()

        email(c.email, render('person/confirmation_email.mako'))

        return render('person/password_confirmation_sent.mako')

    @dispatch_on(POST="_reset_password")
    def reset_password(self, url_hash):
        c.conf_rec = PasswordResetConfirmation.find_by_url_hash(url_hash)

        return render('person/reset.mako')

    @validate(schema=PasswordResetSchema(), form='reset_password', post_only=True, on_get=True, variable_decode=True)
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
        delta = now - c.conf_rec.timestamp
        if delta > datetime.timedelta(hours=24):
            # this confirmation record has expired
            meta.Session.delete(c.conf_rec)
            meta.Session.commit()
            return render('person/expired.mako')

        c.person = Person.find_by_email(c.conf_rec.email_address)
        if c.person is None:
            raise RuntimeError, "Person doesn't exist %s" % c.conf_rec.email_address

        # set the password
        c.person.password = self.form_result['password']
        # also make sure the person is activated
        c.person.activated = True

        # delete the conf rec
        meta.Session.delete(c.conf_rec)
        meta.Session.commit()

        h.flash('Your password has been updated!')
        self.finish_login(c.person.email_address)


    @authorize(h.auth.is_valid_user)
    @dispatch_on(POST="_finish_signup")
    def finish_signup(self):
        c.form = 'finish_signup'

        c.person = h.signed_in_person()
        c.social_networks = SocialNetwork.find_all()
        c.person.fetch_social_networks()

        defaults = h.object_to_defaults(c.person, 'person')
        defaults['person.email_address2'] = c.person.email_address
        if not defaults['person.country']:
            defaults['person.country'] = 'AUSTRALIA'

        form = render('/person/finish_signup.mako')
        return htmlfill.render(form, defaults)


    @authorize(h.auth.is_valid_user)
    @validate(schema=UpdatePersonSchema(), form='finish_signup', post_only=True, on_get=True, variable_decode=True)
    def _finish_signup(self):
        c.person = h.signed_in_person()
        self.finish_edit(c.person)

        redirect_location = session.pop('redirect_to', None)
        if redirect_location:
            redirect_to(str(redirect_location))
        else:
            redirect_to('home')

    def finish_edit(self, person):
        for key in self.form_result['person']:
            setattr(person, key, self.form_result['person'][key])

        for sn in self.form_result['social_network']:
           network = SocialNetwork.find_by_name(sn['name'])
           if sn['account_name']:
               person.social_networks[network] = sn['account_name']
           elif network in person.social_networks:
               del person.social_networks[network]

        # update the objects with the validated form data
        meta.Session.commit()

    @authorize(h.auth.is_valid_user)
    @dispatch_on(POST="_edit")
    def edit(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()
        c.form = 'edit'
        c.person = Person.find_by_id(id)
        c.social_networks = SocialNetwork.find_all()
        c.person.fetch_social_networks()

        defaults = h.object_to_defaults(c.person, 'person')
        defaults['person.email_address2'] = c.person.email_address
        if not defaults['person.country']:
            defaults['person.country'] = 'AUSTRALIA'

        form = render('/person/edit.mako')
        return htmlfill.render(form, defaults)


    @authorize(h.auth.is_valid_user)
    @validate(schema=UpdatePersonSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        """UPDATE PERSON"""
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.person = Person.find_by_id(id)
        self.finish_edit(c.person)

        redirect_to(action='view', id=id)

    @authorize(h.auth.is_valid_user)
    def reprint(self, id):
        c.person = Person.find_by_id(id)
        c.person.badge_printed = False
        meta.Session.commit()
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_new")
    def new(self):
        # Do we allow account creation?
        if lca_info['account_creation']:
            """Create a new person form.
            """
            if h.signed_in_person():
                h.flash("You're already logged in")
                redirect_to('home')

            defaults = {
                'person.country': 'AUSTRALIA',
            }
            if h.lca_rego['personal_info']['home_address'] == 'no':
                defaults['person.address1'] = 'not available'
                defaults['person.city'] = 'not available'
                defaults['person.postcode'] = 'not available'

            c.social_networks = SocialNetwork.find_all()

            form = render('/person/new.mako')
            return htmlfill.render(form, defaults)
        else:
            return render('/not_allowed.mako')

    @validate(schema=NewPersonSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        # Do we allow account creation?
        if lca_info['account_creation']:
            """Create a new person submit.
            """

            # Remove fields not in class
            results = self.form_result['person']
            del results['password_confirm']
            del results['email_address2']
            c.person = Person(**results)
            c.person.email_address = c.person.email_address.lower()
            meta.Session.add(c.person)

            #for sn in self.form_result['social_network']:
            #   network = SocialNetwork.find_by_name(sn['name'])
            #   if sn['account_name']:
            #       c.person.social_networks[network] = sn['account_name']

            meta.Session.commit()

            if lca_rego['confirm_email_address'] == 'no':
                redirect_to(controller='person', action='confirm', confirm_hash=c.person.url_hash)
            else:
                email(c.person.email_address, render('/person/new_person_email.mako'))
                return render('/person/thankyou.mako')
        else:
            return render('/not_allowed.mako')

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_new_incomplete")
    def new_incomplete(self):
        return render('/person/new_incomplete.mako')

    @validate(schema=NewIncompletePersonSchema(), form='new_incomplete', post_only=True, on_get=True, variable_decode=True)
    def _new_incomplete(self):
        results = self.form_result['person']
        del results['email_address2']
        c.person = Person(**results)
        c.person.email_address = c.person.email_address.lower()
        meta.Session.add(c.person)
        meta.Session.commit()
        redirect_to(controller='person', action='index')

    @authorize(h.auth.has_organiser_role)
    def index(self):
        c.person_collection = Person.find_all()
        return render('/person/list.mako')

    @authorize(h.auth.is_valid_user)
    def view(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(id), h.auth.has_reviewer_role, h.auth.has_organiser_role)):
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
    @validate(schema=RoleSchema, form='roles', post_only=True, on_get=True, variable_decode=True)
    def _roles(self, id):
        """ Lists and changes the person's roles. """

        c.person = Person.find_by_id(id)
        c.roles = Role.find_all()

        role = self.form_result['role']
        action = self.form_result['action']

        role = Role.find_by_name(name=role)

        if action == 'Revoke' and role in c.person.roles:
            c.person.roles.remove(role)
            h.flash('Role ' + role.name + ' Revoked')
        elif action == 'Grant' and role not in c.person.roles:
            c.person.roles.append(role)
            h.flash('Role ' + role.name + ' Granted')
        else:
            h.flash("Nothing to do")

        meta.Session.commit()

        return render('person/roles.mako')

    @dispatch_on(POST="_offer")
    @authorize(h.auth.is_valid_user)
    def offer(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(id), h.auth.has_reviewer_role, h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()
        c.person = Person.find_by_id(id)
        c.offers = c.person.proposal_offers
        c.travel_assistance = reduce(lambda a, b: a or ('Travel' in b.status.name), c.offers, False) or False 
        c.accommodation_assistance = reduce(lambda a, b: a or ('Accommodation' in b.status.name), c.offers, False) or False 

        # Set initial form defaults
        defaults = {
            'status': 'accept',
            }
        if c.person.travel:
            defaults.update(h.object_to_defaults(c.person.travel, 'travel'))

        form = render('person/offer.mako')
        return htmlfill.render(form, defaults)

    @authorize(h.auth.is_valid_user)
    @validate(schema=OfferSchema, form='offer', post_only=True, on_get=True, variable_decode=True)
    def _offer(self,id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(id), h.auth.has_reviewer_role, h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()
        c.person = Person.find_by_id(id)
        c.offers = c.person.proposal_offers
        c.travel_assistance = reduce(lambda a, b: a or ('Travel' in b.status.name), c.offers, False) or False 
        c.accommodation_assistance = reduce(lambda a, b: a or ('Accommodation' in b.status.name), c.offers, False) or False 

        # What status are we moving all proposals to?
        if self.form_result['status'] == 'accept':
            c.status = ProposalStatus.find_by_name('Accepted')
        elif self.form_result['status'] == 'withdraw':
            c.status = ProposalStatus.find_by_name('Withdrawn')
        elif self.form_result['status'] == 'contact':
            c.status = ProposalStatus.find_by_name('Contact')
        else:
            c.status = None

        for offer in c.person.proposal_offers:
            offer.status = c.status

        if c.travel_assistance:
            if not c.person.travel:
                self.form_result['travel']['flight_details'] = ''
                travel = Travel(**self.form_result['travel'])
                meta.Session.add(travel)
                c.person.travel = travel
            else:
                for key in self.form_result['travel']:
                    setattr(c.person.travel, key, self.form_result['travel'][key])

        if c.status.name == 'Accepted':
            email(c.person.email_address, render('/person/offer_email.mako'))
        else:
            email([c.person.email_address, h.lca_info['emails']['presentation']], render('/person/offer_email.mako'))

        # update the objects with the validated form data
        meta.Session.commit()
        return render('person/offer.mako')
