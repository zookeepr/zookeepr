import datetime
import md5

from zookeepr.model.core import PasswordResetConfirmation
from zookeepr.tests.model import *

class TestPasswordResetConfirmation(ModelTest):
    domain = model.PasswordResetConfirmation
    samples = [dict(email_address='testguy@example.org'),
        dict(email_address='testgirl@example.org'),
        ]
