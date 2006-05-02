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
        
        ## submit the form
        u = url_for(controller='/cfp', action='new')
        params = {'cfp.handle': 'testguy',
                  'cfp.firstname': 'Testguy',
                  'cfp.lastname': 'McTest',
                  'cfp.type': 'Paper',
                  'cfp.title': 'My Awesome Paper',
                  'cfp.abstract': 'Some abstract'}
        res = self.app.post(u, params=params)

        ## check that it's in the database
        ps = Person.select_by(handle='testguy')
        self.failIf(len(ps) == 0, "person object not in database")
        self.failUnless(len(ps) == 1, "too many person objects in database")

        ss = Submission.select_by(person=ps[0])
        self.failIf(len(ss) == 0, "submission object not in database")
        self.failUnless(len(ss) == 1, "too many submission objects in database")
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
