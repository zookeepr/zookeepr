# Zookeepr driver for AuthKit
#
# This module allows us to use the authkit infrastructure but using the Zookeepr models to do so
#  * We don't support groups
#  * We don't support the creation methods as zookeepr does that already
#
# Based on
# SQLAlchemy 0.5 Driver for AuthKit
# Based on the SQLAlchemy 0.4.4 driver but using session.add() instead of 
# session.save()

# This file assumes the following in the model used in Pylons 0.9.7

#from authkit.users import *

#import sqlalchemy as sa
#from sqlalchemy.orm import *
#
#
#from zookeepr.model.person import Person
#from zookeepr.model.role import Role
#


import logging

from pylons.templating import render_mako as render
from pylons import tmpl_context as c
from pylons import request

from formencode import validators, htmlfill, Invalid
from zookeepr.lib.validators import BaseSchema

from zookeepr.model import meta
from zookeepr.model import Person, Role

from authkit.permissions import HasAuthKitRole, UserIn, NotAuthenticatedError

import md5

log = logging.getLogger(__name__)

class LoginSchema(BaseSchema):
    username = validators.Email(not_empty=True)
    password = validators.String(not_empty=True)

def render_signin(environ):
    if 'auth_failure' in environ:
        c.auth_failure = environ['auth_failure']
    else:
        c.auth_failure = None

    errors = {}
    defaults = dict(request.params)
    if defaults:
        try:
            LoginSchema.to_python(defaults)
        except Invalid, error:
            defaults = error.value
            errors = error.error_dict or {}

    form = render('/person/signin.mako')
    return htmlfill.render(form, defaults=defaults, errors=errors).replace('%', '%%').replace('FORM_ACTION', '%s')


def encrypt(password):
    return md5.new(password).hexdigest()


def valid_password(environ, username, password):
    """
    A function which can be used with the ``basic`` and ``form`` authentication
    methods to validate a username and passowrd.

    In this implementation usernames are case insensitive and passwords are
    case sensitive. The function returns ``True`` if the user ``username`` has
    the password specified by ``password`` and returns ``False`` if the user
    doesn't exist or the password is incorrect.
    """

    person = Person.find_by_email(username)

    if person is None:
        environ['auth_failure'] = 'NO_USER'
        return False

    if not person.activated:
        environ['auth_failure'] = 'NOT_ACTIVATED'
        return False

    if not person.check_password(password):
        environ['auth_failure'] = 'BAD_PASSWORD'
        return False

    return True


class ValidZookeeprUser(UserIn):
    """
    Checks that the signed in user is one of the users specified when setting up
    the user management API.
    """
    def __init__(self):
        pass

    def check(self, app, environ, start_response):

        if not environ.get('REMOTE_USER'):
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
            raise NotAuthenticatedError('Not authenticated')

        for role in self.roles:
           if not self.role_exists(role):
               raise Exception("No such role %r exists"%role)

        if self.all:
            for role in self.roles:
                if not self.user_has_role(environ['REMOTE_USER'], role):
                    if self.error:
                        raise self.error
                    else:
                        raise NotAuthorizedError(
                            "User doesn't have the role %s"%role.lower()
                        )
            return app(environ, start_response)
        else:
            for role in self.roles:
                if self.user_has_role(environ['REMOTE_USER'], role):
                    return app(environ, start_response)
            if self.error:
                raise self.error
            else:
                raise NotAuthorizedError(
                    "User doesn't have any of the specified roles"
                )

    def user_exists(self, username):
        """
        Returns ``True`` if the user exists, ``False`` otherwise. Users are
        case insensitive.
        """

        person = Person.find_by_email(username)

        if person is not None:
            return True
        return False

    def role_exists(self, role):
        """
        Returns ``True`` if the role exists, ``False`` otherwise. Roles are
        case insensitive.
        """
        role = Role.find_by_name(role)

        if role is not None:
            return True
        return False

    def user_has_role(self, username, role):
        """
        Returns ``True`` if the user has the role specified, ``False`` 
        otherwise. Raises an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        if not self.role_exists(role.lower()):
            raise AuthKitNoSuchRoleError("No such role %r"%role.lower())
        person = Person.find_by_email(username)
        for role_ in person.roles:
            if role_.name == role.lower():
                return True
        return False


# Role shortcuts to save db work
has_organiser_role = HasZookeeprRole('organiser')
has_reviewer_role = HasZookeeprRole('reviewer')
has_planetfeed_role = HasZookeeprRole('planetfeed')
has_keysigning_role = HasZookeeprRole('keysigning')
is_valid_user = ValidZookeeprUser()


