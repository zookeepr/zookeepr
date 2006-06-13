import md5

from zookeepr.tests.functional import *

class TestCFP(ControllerTest):
    model = model.CFP
    name = 'cfp'
    url = '/cfp'
    samples = [dict(email_address='testguy@example.org',
                    password='password',
                    password_confirm='password',
                    title='title yo',
                    abstract='abstract yo',
                    url='http://example.org',
                    attachment='foo',
                    ),
               dict(email_address='testgirl@example.org',
                    password='snuh',
                    password_confirm='snuh',
                    title='some title',
                    abstract='some abstract',
                    url='http://example.com',
                    attachment='bar',
                    ),
               ]
    no_test = ['password_confirm', 'attachment']
    mangles = dict(password = lambda p: md5.new(p).hexdigest())
