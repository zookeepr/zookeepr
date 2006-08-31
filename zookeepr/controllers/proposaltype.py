from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema
from zookeepr.model import ProposalType

class ProposalTypeSchema(Schema):
    name = validators.String(not_empty=True)

class NewProposalTypeSchema(BaseSchema):
    proposaltype = ProposalTypeSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditProposalTypeSchema(BaseSchema):
    proposaltype = ProposalTypeSchema()
    pre_validators = [variabledecode.NestedVariables]

class ProposaltypeController(SecureController, View, Modify):
    schemas = {"new" : NewProposalTypeSchema(),
               "edit" : EditProposalTypeSchema()}
    permissions = {"view": [AuthRole('site-admin')],
                   "index": [AuthRole('site-admin')],
                   "edit": [],
                   "delete": [],
                   "new": [],
                   }

    model = ProposalType
    individual = 'proposaltype'
    redirect_map = dict(new=dict(action='index'))
