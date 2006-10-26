from zookeepr.tests.functional import *

class TestRegistrationController(ControllerTest):
    model = model.registration.Registration
    url = '/registration'
    param_name = 'registration'
    samples = [dict(
        registration=dict(address1='a1',
            address2='a2',
            city='city',
            state='state1',
            country='country1',
            postcode='postcode1',
            company='company1',
            shelltext='shelltext1',
            editortext='editortext1',
            distrotext='distrotext1',
            type='Professional',
            discount_code='discount_code1',
            teesize='M_M',
            diet='diet1',
            special='special1',
            opendaydrag=1,
            partner_email='partneremail1',
            kids_0_3=1,
            kids_4_6=1,
            kids_7_9=1,
            kids_10=1,
            checkin=14,
            checkout=20,
            lasignup=True,
            announcesignup=True,
            delegatesignup=False,
            editor='-',
            distro='-',
            shell='-',
            accommodation='own',
            ),
            person=dict(

            email_address='testguy@example.org',
            password='test',
            password_confirm='test',
            handle='testguy',
            fullname='testguy mctest',
            )
            )]
    no_test = ['password_confirm', 'person']
    crud = ['create']

    def tearDown(self):
        ps = Query(model.Person).select()
        for p in ps:
            objectstore.delete(p)
        objectstore.flush()
