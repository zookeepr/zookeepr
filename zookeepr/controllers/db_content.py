import logging
from formencode import validators, variabledecode
from formencode.schema import Schema
from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *
from zookeepr.lib.validators import BaseSchema, BoundedInt
from zookeepr.lib.base import *

log = logging.getLogger(__name__)

class DbContentSchema(BaseSchema):
    title = validators.String(not_empty=True)
    url = validators.String(not_empty=True)
    body = validators.String(not_empty=True)

class NewContentSchema(BaseSchema):
    db_content = DbContentSchema()
    pre_validators = [variabledecode.NestedVariables]

class UpdateContentSchema(BaseSchema):
    db_content = DbContentSchema()
    pre_validators = [variabledecode.NestedVariables]


class DbContentController(SecureController, Create, List, Read, Update):
    individual = 'db_content'
    model = model.DBContent
    schemas = {'new': NewContentSchema(),
               'edit': UpdateContentSchema()
              }

    permissions = {'new': [AuthRole('organiser')],
                   'index': [AuthRole('organiser')],
                   'view': [AuthTrue()],
                   'edit': [AuthRole('organiser')]
                   }
                   
    def __before__(self, **kwargs):
        super(DbContentController, self).__before__(**kwargs)
        c.dbsession = self.dbsession # for the use of list.myt

