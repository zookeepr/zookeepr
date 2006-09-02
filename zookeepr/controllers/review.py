from zookeepr.lib.base import BaseController, render_response, model
from zookeepr.lib.crud import List

class ReviewController(BaseController, List):
    model = model.Review
    individual = 'review'
    permissions = {'index': [AuthRole('reviewer')],
                   }
