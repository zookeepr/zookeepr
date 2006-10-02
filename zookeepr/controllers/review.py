from zookeepr.lib.auth import AuthRole, SecureController
from zookeepr.lib.base import render_response, model
from zookeepr.lib.crud import List, Update

class ReviewController(SecureController, List, Update):
    model = model.Review
    individual = 'review'
    permissions = {'index': [AuthRole('reviewer')],
                   'edit': [AuthRole('reviewer')],
                   }
