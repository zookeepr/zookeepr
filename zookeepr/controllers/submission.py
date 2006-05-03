from zookeepr.lib.base import *

class SubmissionController(BaseController, View, Modify):
    model = model.Submission
    conditions = dict(order_by='title')
