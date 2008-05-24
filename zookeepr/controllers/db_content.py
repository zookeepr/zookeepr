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

class DbContentController(Create):

    schemas = {'new': DbContentSchema(),
              }

    permissions = {'new': [AuthRole('organiser')]
                   }
    
    



