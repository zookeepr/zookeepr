import unittest

from zkpylons.lib.validators import *

class TestEmailAddressValidator(unittest.TestCase):

    def test_localhost(self):
        v = EmailAddress()
        v.validate_python('test@localhost', None)

    def test_exampleorg(self):
        v = EmailAddress()
        v.validate_python('test@example.org', None)
