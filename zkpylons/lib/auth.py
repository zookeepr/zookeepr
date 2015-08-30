# Zookeepr driver for AuthKit
#
# This module allows us to use the authkit infrastructure but using the
# Zookeepr models to do so
#  * We don't support groups
#  * We don't support the creation methods as zkpylons does that already
#


import logging

from pylons.templating import render_mako as render
from pylons import tmpl_context as c
from pylons import request

from formencode import validators, htmlfill, Invalid
from zkpylons.lib.validators import BaseSchema

from zkpylons.model import meta
from zkpylons.model import Person, Role, Proposal, Invoice, Registration, Funding, URLHash

from authkit import users
from authkit.permissions import HasAuthKitRole, UserIn, NotAuthenticatedError, NotAuthorizedError, Permission, PermissionError
from authkit.authorize import PermissionSetupError, middleware
from authkit.authorize.pylons_adaptors import authorized

from pylons import request, response, session
from pylons.controllers.util import redirect, abort
from pylons import url

import hashlib

log = logging.getLogger(__name__)

def set_redirect():
    # TODO: This function is called 30+ times per page when not logged in, more than seems needed
    if not session.get('redirect_to', None):
        session['redirect_to'] =  request.path_info
        session.save()

def set_role(msg):
    if not session.get('role_error', None):
        session['role_error'] = msg
        session.save()


class ValidZookeeprUser(UserIn):
    """
    Checks that the signed in user is one of the users specified when setting up
    the user management API.
    """
    def __init__(self):
        pass

    def check(self, app, environ, start_response):

        if not environ.get('REMOTE_USER'):
            set_redirect()
            raise NotAuthenticatedError('Not Authenticated')

        person = Person.find_by_email(environ['REMOTE_USER'])
        if Person is None:
            environ['auth_failure'] = 'NO_USER'
            raise NotAuthorizedError(
                'You are not one of the users allowed to access this resource.'
            )

        return app(environ, start_response)

class HasZookeeprRole(HasAuthKitRole):
    def check(self, app, environ, start_response):
        """
        Should return True if the user has the role or
        False if the user doesn't exist or doesn't have the role.

        In this implementation role names are case insensitive.
        """

        if not environ.get('REMOTE_USER'):
            if self.error:
                raise self.error
            set_redirect()
            raise NotAuthenticatedError('Not authenticated')

        for role in self.roles:
           if not self.role_exists(role):
               raise NotAuthorizedError("No such role %r exists"%role)

        person = Person.find_by_email(environ['REMOTE_USER'])
        if person is None:
            raise users.AuthKitNoSuchUserError(
                "No such user %r" % environ['REMOTE_USER'])

        if not person.activated:
            #set_role('User account must be activated')
            raise NotAuthorizedError(
                    "User account must be activated"
                )

        if self.all:
            for role in self.roles:
                if not self.user_has_role(person, role):
                    if self.error:
                        raise self.error
                    else:
                        set_role("User doesn't have the role %s"%role.lower())
                        raise NotAuthorizedError(
                            "User doesn't have the role %s"%role.lower()
                        )
            return app(environ, start_response)
        else:
            for role in self.roles:
                if self.user_has_role(person, role):
                    return app(environ, start_response)
            if self.error:
                raise self.error
            else:
                set_role("User doesn't have any of the specified roles")
                raise NotAuthorizedError(
                    "User doesn't have any of the specified roles"
                )

    def role_exists(self, role):
        """
        Returns ``True`` if the role exists, ``False`` otherwise. Roles are
        case insensitive.
        """
        role = Role.find_by_name(role)

        if role is not None:
            return True
        return False

    def user_has_role(self, person, role):
        """
        Returns ``True`` if the user has the role specified, ``False``
        otherwise. Raises an exception if the user doesn't exist.
        """
        if not self.role_exists(role.lower()):
            raise users.AuthKitNoSuchRoleError("No such role %r"%role.lower())

        for role_ in person.roles:
            if role_.name == role.lower():
                return True
        return False


class IsSameZookeeprUser(UserIn):
    """
    Checks that the signed in user is one of the users specified when setting up
    the user management API.
    """
    def __init__(self, id):
        self.id = int(id)

    def check(self, app, environ, start_response):

        if not environ.get('REMOTE_USER'):
            set_redirect()
            raise NotAuthenticatedError('Not Authenticated')

        person = Person.find_by_email(environ['REMOTE_USER'])
        if person is None:
            environ['auth_failure'] = 'NO_USER'
            raise NotAuthorizedError(
                'You are not one of the users allowed to access this resource.'
            )

        if self.id != person.id:
            set_role("User doesn't have any of the specified role")
            raise NotAuthorizedError(
                "User doesn't have any of the specified roles"
            )

        return app(environ, start_response)


class IsActivatedZookeeprUser(UserIn):
    """
    Checks that the signed in user is activated
    """

    def __init__(self):
        pass

    def check(self, app, environ, start_response):
        if not environ.get('REMOTE_USER'):
            set_redirect()
            raise NotAuthenticatedError('Not Authenticated')

        person = Person.find_by_email(environ['REMOTE_USER'])
        if person is None:
            set_redirect()
            environ['auth_failure'] = 'NO_USER'
            raise NotAuthorizedError(
                'You are not one of the users allowed to access this resource.'
            )

        if not person.activated:
            set_redirect()
            if 'is_active' in dir(meta.Session):
                meta.Session.flush()
                meta.Session.close()

            redirect(url(controller="person", action="activate"))

        return app(environ, start_response)


class IsSameZookeeprSubmitter(UserIn):
    """
    Checks that the signed in user is one of the users specified when setting up
    the user management API.
    """
    def __init__(self, proposal_id):
        self.proposal_id = int(proposal_id)

    def check(self, app, environ, start_response):

        if not environ.get('REMOTE_USER'):
            set_redirect()
            raise NotAuthenticatedError('Not Authenticated')

        person = Person.find_by_email(environ['REMOTE_USER'])
        if person is None:
            environ['auth_failure'] = 'NO_USER'
            raise NotAuthorizedError(
                'You are not one of the users allowed to access this resource.'
            )

        proposal = Proposal.find_by_id(self.proposal_id)
        if proposal is None:
            raise NotAuthorizedError(
                "Proposal doesn't exist"
            )

        if person not in proposal.people:
            set_role("User doesn't have any of the specified roles")
            raise NotAuthorizedError(
                "User doesn't have any of the specified roles"
            )

        return app(environ, start_response)

class IsSameZookeeprFundingSubmitter(UserIn):
    """
    Checks that the signed in user is one of the users specified when setting up
    the user management API.
    """
    def __init__(self, funding_id):
        self.funding_id = int(funding_id)

    def check(self, app, environ, start_response):

        if not environ.get('REMOTE_USER'):
            raise NotAuthenticatedError('Not Authenticated')

        person = Person.find_by_email(environ['REMOTE_USER'])
        if person is None:
            environ['auth_failure'] = 'NO_USER'
            raise NotAuthorizedError(
                'You are not one of the users allowed to access this resource.'
            )

        funding = Funding.find_by_id(self.funding_id)
        if funding is None:
            raise NotAuthorizedError(
                "Funding Request doesn't exist"
            )

        if person != funding.person:
            set_role("User doesn't have any of the specified roles")
            raise NotAuthorizedError(
                "User doesn't have any of the specified roles"
            )

        return app(environ, start_response)

class IsSameZookeeprAttendee(UserIn):
    """
    Checks that the signed in user is the user for which the given invoice
    is for.
    """
    def __init__(self, invoice_id):
        self.invoice_id = int(invoice_id)

    def check(self, app, environ, start_response):

        if not environ.get('REMOTE_USER'):
            set_redirect()
            raise NotAuthenticatedError('Not Authenticated')

        person = Person.find_by_email(environ['REMOTE_USER'])
        if person is None:
            environ['auth_failure'] = 'NO_USER'
            raise NotAuthorizedError(
                'You are not one of the users allowed to access this resource.'
            )

        invoice = Invoice.find_by_id(self.invoice_id)
        if invoice is None:
            raise NotAuthorizedError(
                "Invoice doesn't exist"
            )

        if person.id <> invoice.person_id:
            set_role("Invoice is not for this user")
            raise NotAuthorizedError(
                "Invoice is not for this user"
            )

        return app(environ, start_response)

class HasUniqueKey(Permission):
    def check(self, app, environ, start_response):
        url = request.path
        fields = dict(request.GET)
        if fields.has_key('hash'):
            dburl = URLHash.find_by_hash(fields['hash']).url
            if dburl is not None:
                if url.startswith(dburl):
                    return app(environ, start_response)
        raise NotAuthorizedError(
            "You are not authorised to view this page"
        )

class IsSameZookeeprRegistration(UserIn):
    """
    Checks that the signed in user is the user this registration belongs
    to.
    """
    def __init__(self, registration_id):
        self.registration_id = int(registration_id)

    def check(self, app, environ, start_response):

        if not environ.get('REMOTE_USER'):
            set_redirect()
            raise NotAuthenticatedError('Not Authenticated')

        person = Person.find_by_email(environ['REMOTE_USER'])
        if person is None:
            environ['auth_failure'] = 'NO_USER'
            raise NotAuthorizedError(
                'You are not one of the users allowed to access this resource.'
            )

        registration = Registration.find_by_id(self.registration_id)
        if registration is None:
            raise NotAuthorizedError(
                "Registration doesn't exist"
            )

        if person.id <> registration.person_id:
            set_role("Registration is not for this user");
            raise NotAuthorizedError(
                "Registration is not for this user"
            )

        return app(environ, start_response)

class Or(Permission):
    """
    Checks all the permission objects listed as keyword arguments in turn.
    Permissions are checked from left to right. The error raised by the ``Or``
    permission is the error raised by the first permission check to fail.
    """

    def __init__(self, *permissions):
        if len(permissions) < 2:
            raise PermissionSetupError('Expected at least 2 permissions objects')
        permissions = list(permissions)
        self.permissions = permissions

    def check(self, app, environ, start_response):
        for permission in self.permissions:
            try:
                permission.check(app, environ, start_response)
                return app(environ, start_response)
            except (NotAuthenticatedError, NotAuthorizedError):
                pass

        raise NotAuthorizedError(
                'You are not one of the users allowed to access this resource.'
        )

def no_role():
    set_role("User doesn't have any of the specified roles")
    raise NotAuthorizedError(
            "User doesn't have any of the specified roles"
            )


# Role shortcuts to save db work
has_organiser_role = HasZookeeprRole('organiser')
has_reviewer_role = HasZookeeprRole('reviewer')
has_funding_reviewer_role = HasZookeeprRole('funding_reviewer')
has_proposals_chair_role = HasZookeeprRole('proposals_chair')
has_late_submitter_role = HasZookeeprRole('late_submitter')
has_planetfeed_role = HasZookeeprRole('planetfeed')
has_keysigning_role = HasZookeeprRole('keysigning')
has_checkin_role = HasZookeeprRole('checkin')
is_valid_user = ValidZookeeprUser()
is_activated_user = IsActivatedZookeeprUser()
is_same_zkpylons_user = IsSameZookeeprUser
is_same_zkpylons_submitter = IsSameZookeeprSubmitter
is_same_zkpylons_attendee = IsSameZookeeprAttendee
is_same_zookeepr_registration = IsSameZookeeprRegistration
is_same_zkpylons_funding_submitter = IsSameZookeeprFundingSubmitter
has_unique_key = HasUniqueKey
