from zookeepr.tests import *
from zookeepr.models import *

class TestCfpController(TestController):
    
    #def test_index(self):
        #response = self.app.get(url_for(controller='cfp'))
        # Test response...
        #response.mustcontain("perhaps you'd like to")
    #    pass

    def test_create(self):
        """Test create action on /cfp"""

        ## set us up a submission type
        st = SubmissionType('Paper')
        
        u = url_for(controller='/cfp')

        # get the form
        res = self.app.get(u)

        ## submit the form
        params = {'person.handle': 'testguy',
                  'person.firstname': 'Testguy',
                  'person.lastname': 'McTest',
                  'person.email_address': 'testguy@example.org',
                  'person.password': 'p4ssw0rd',
                  'person.password_confirm': 'p4ssw0rd',
                  'submission.submission_type': 'Paper',
                  'submission.title': 'My Awesome Paper',
                  'submission.experience': 'Plenty',
                  'submission.url': 'http://example.org',
                  'submission.abstract': 'Very'}
        files = [('submission.attachment', 'test.txt', """I am a test file""")]
        res = self.app.post(u, params=params, upload_files=files)

        ## check that it's in the database
        ps = Person.select_by(handle='testguy')
        self.failIf(len(ps) == 0, "person object not in database")
        self.failUnless(len(ps) == 1, "too many person objects in database")

        self.failUnless(ps[0].handle == 'testguy')
        self.failUnless(ps[0].firstname == 'Testguy')
        self.failUnless(ps[0].lastname == 'McTest')
        self.failUnless(ps[0].email_address == 'testguy@example.org')
        self.failUnless(ps[0].password_hash == md5.new('p4ssw0rd').hexdigest())

        ss = Submission.select_by(title='My Awesome Paper')
        self.failIf(len(ss) == 0, "submission object not in database")
        self.failUnless(len(ss) == 1, "too many submission objects in database")

        self.failUnless(ss[0].title == 'My Awesome Paper')
        self.failUnless(ss[0].experience == 'Plenty')
        self.failUnless(ss[0].url == 'http://example.org')
        self.failUnless(ss[0].abstract == 'Very')
        self.failUnless(ss[0].submission_type == 'Paper')
        self.assertEqual(ss[0].attachment, """I am a test file""")
        
        self.failUnless(ss[0] in ps[0].submissions, "submission not attributed to person")

        # clean up
        ps[0].delete()
        st.delete()
        objectstore.commit()
        # check
        ss = Submission.select()
        self.failUnless(len(ss) == 0, "submission database not empty")
        ps = Person.select()
        self.failUnless(len(ps) == 0, "person database not empty")
        sts = SubmissionType.select()
        self.failUnless(len(sts) == 0, "submissino type database not empty")
