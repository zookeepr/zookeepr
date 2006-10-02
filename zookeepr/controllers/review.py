from formencode import variabledecode

from zookeepr.lib.auth import AuthRole, SecureController
from zookeepr.lib.base import render_response, model
from zookeepr.lib.crud import List, Update
from zookeepr.lib.validators import BaseSchema, ReviewSchema

class EditReviewSchema(BaseSchema):
    review = ReviewSchema()
    pre_validators = [variabledecode.NestedVariables]

class ReviewController(SecureController, List, Update):
    model = model.Review
    individual = 'review'
    permissions = {'index': [AuthRole('reviewer')],
                   'edit': [AuthRole('reviewer')],
                   }
    schemas = {'edit': EditReviewSchema(),
               }
