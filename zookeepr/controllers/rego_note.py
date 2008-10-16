import logging
from formencode import validators, variabledecode
from formencode.schema import Schema
from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *
from zookeepr.lib.validators import *
from zookeepr.lib.base import *
from zookeepr.controllers import not_found
from zookeepr.model.db_content import DBContentType
from pylons import response
from zookeepr.config.lca_info import file_paths
import os
import cgi

from webhelpers.pagination import paginate

log = logging.getLogger(__name__)

class RegoNoteSchema(BaseSchema):
    rego = ExistingRegistrationValidator(not_empty=True)
    note = validators.String(not_empty=True)
    by = ExistingPersonValidator(not_empty=True)

class NewNoteSchema(BaseSchema):
    rego_note = RegoNoteSchema()
    pre_validators = [variabledecode.NestedVariables]

class UpdateNoteSchema(BaseSchema):
    rego_note = RegoNoteSchema()
    pre_validators = [variabledecode.NestedVariables]

class RegoNoteController(SecureController, Create, List, Read, Update, Delete):
    individual = 'rego_note'
    model = model.RegoNote
    schemas = {'new': NewNoteSchema(),
               'edit': UpdateNoteSchema()
              }

    permissions = {'new': [AuthRole('organiser')],
                   'index': [AuthRole('organiser')],
                   'view': [AuthRole('organiser')],
                   'edit': [AuthRole('organiser')],
                   'delete': [AuthRole('organiser')]
                   }

    def new(self, id=None):
        if hasattr(super(RegoNoteController, self), 'new'):
            return super(RegoNoteController, self).new()
