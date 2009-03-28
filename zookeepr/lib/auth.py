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

from paste.util.import_string import eval_import
from authkit.users import *

import sqlalchemy as sa
from sqlalchemy.orm import *

from zookeepr.model import meta

from zookeepr.model.person import Person
from zookeepr.model.role import Role

import md5

from pylons.templating import render_mako as render
from pylons import tmpl_context as c

from authkit.permissions import HasAuthKitRole

def render_signin(environ):
    c.auth_failed = False

    if environ['CONTENT_TYPE'] == 'application/x-www-form-urlencoded':
        c.auth_failed = True

    return render('/person/signin.mako')


def encrypt(password, secret):
    return md5.new(password).hexdigest()

# Role shortcuts to save db work
has_organiser_role = HasAuthKitRole('organiser')


class UsersFromZookeepr(): #authkit.users.Users):
    """
    Database Version
    """
    def __init__(self, model, encrypt=None):
        if encrypt is None:
            def encrypt(password):
                return password
        self.encrypt = encrypt

        if isinstance(model, (str, unicode)):
            model = eval_import(model)
        if hasattr(model, 'authkit_initialized'):
            raise AuthKitError(
                'The AuthKit database model has already been setup'
            )
        else:
            model.authkit_initialized = True

    # Existence Methods
    def user_exists(self, username):
        """
        Returns ``True`` if a user exists with the given username, ``False`` 
        otherwise. Usernames are case insensitive.
        """

        person = meta.Session.query(Person).filter_by(email_address=username.lower()).first()

        if person is not None:
            return True
        return False

    def role_exists(self, role):
        """
        Returns ``True`` if the role exists, ``False`` otherwise. Roles are
        case insensitive.
        """
        role = meta.Session.query(Role).filter_by(name=role).first()

        if role is not None:
            return True
        return False

    # List Methods
    def list_roles(self):
        """
        Returns a lowercase list of all roll names ordered alphabetically
        """
        return [r.name for r in self.meta.Session.query(Role).order_by(Role.name)]


    def list_users(self):
        """
        Returns a lowecase list of all usernames ordered alphabetically
        """
        return [r.email_address for r in meta.Session.query(Person).order_by(Person.email_address)]

    # User Methods
    def user(self, username):
        """
        Returns a dictionary in the following format:

        .. code-block :: Python
        
            {
                'username': username,
                'group':    group,
                'password': password,
                'roles':    [role1,role2,role3... etc]
            }

        The role names are ordered alphabetically
        Raises an exception if the user doesn't exist.
        """    
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        user = meta.Session.query(Person).filter_by(email_address=username.lower()).first()
        roles = [r.name for r in user.roles]
        roles.sort()
        return {
            'username': user.email_address,
            'group':    None,
            'password': user.password,
            'roles':    roles
        }

    def user_roles(self, username):
        """
        Returns a list of all the role names for the given username ordered 
        alphabetically. Raises an exception if the username doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        roles = [r.name for r in meta.Session.query(Person).filter_by(email_address=username.lower()).first().roles]
        roles.sort()
        return roles

    def user_password(self, username):
        """
        Returns the password associated with the user or ``None`` if no
        password exists. Raises an exception is the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        return meta.Session.query(Person).filter_by(email_address=username.lower()).first().password_hash

    def user_has_role(self, username, role):
        """
        Returns ``True`` if the user has the role specified, ``False`` 
        otherwise. Raises an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        if not self.role_exists(role.lower()):
            raise AuthKitNoSuchRoleError("No such role %r"%role.lower())
        for role_ in meta.Session.query(Person).filter_by(email_address=username.lower()).first().roles:
            if role_.name == role.lower():
                return True
        return False

    def user_has_password(self, username, password):
        """
        Returns ``True`` if the user has the password specified, ``False`` 
        otherwise. Passwords are case sensitive. Raises an exception if the
        user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        user = meta.Session.query(Person).filter_by(email_address=username.lower()).first()
        if user.password_hash == self.encrypt(password):
            return True
        return False


