from zookeepr.tests.model import *

class TestPasswordResetConfirmation(CRUDModelTest):
    domain = model.PasswordResetConfirmation
    samples = [dict(email_address='testguy@example.org'),
        dict(email_address='testgirl@example.org'),
        ]
