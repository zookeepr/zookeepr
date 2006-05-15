from authkit import PylonsSecureController

from zookeepr.lib.base import *

class SubmissiontypeController(BaseController, PylonsSecureController, View, Modify):
    model = model.SubmissionType
    individual = 'submissiontype'
    conditions = dict(order_by='name')
