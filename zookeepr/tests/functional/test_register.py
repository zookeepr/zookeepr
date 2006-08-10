import datetime
import md5

from zookeepr.model import Person
from zookeepr.tests.functional import *

class TestRegisterController(ControllerTest):

    def test_registration_confirmation(self):
        # insert registration model object
        timestamp = datetime.datetime.now()
        email_address = 'testguy@testguy.org'
        password = 'password'
        r = Person(creation_timestamp=timestamp,
                   email_address=email_address,
                   password=password,
                   activated=False)
        url_hash = r.url_hash
        print url_hash
        r.save()
        r.flush()
        rid = r.id
        print r
        # clear so that we reload the object later
        objectstore.clear()
        
        # visit the link
        response = self.app.get('/register/confirm/' + url_hash)
        response.mustcontain('Thanks for confirming your registration')
        
        # test that it's activated
        r = Person.get(rid)
        self.assertEqual(True, r.activated, "registration was not activated")

        # clean up
        r = Person.get(rid)
        r.delete()
        r.flush()

    def test_registration_confirmation_invalid_url_hash(self):
        """test that an invalid has doesn't activate anything"""
        self.assertEmptyModel(Person)

        response = self.app.get('/register/confirm/nonexistent', status=404)
