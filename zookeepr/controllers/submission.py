from zookeepr.lib.base import *

class SubmissionController(BaseController, View, Modify):
    individual = 'submission'
    model = model.Submission
    conditions = dict(order_by='title')
