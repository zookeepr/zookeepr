import pprint

from zookeepr.model import Submission, SubmissionType, Person
from zookeepr.tests.functional import *

class TestSubmission(ControllerTest):
    model = Submission
    name = 'submission'
    url = '/submission'
    samples = [dict(title='test',
                    abstract='abstract 1',
                    experience='experience 1',
                    url='http://example.org',
                    ),
               dict(title='not a test',
                    abstract='abstract 2',
                    experience='experience 2',
                    url='http://lca2007.linux.org.au',
                    ),
               ]

    def additional(self, obj):
        obj.people.append(self.p)
        obj.type = self.objectstore.get(SubmissionType, 1)
        return obj
    
    def setUp(self):
        super(TestSubmission, self).setUp()
        model.submission.tables.submission_type.insert().execute(
            dict(id=1, name='Paper'),
            )
        model.submission.tables.submission_type.insert().execute(
            dict(id=2, name='Presentation'),
            )
        model.submission.tables.submission_type.insert().execute(
            dict(id=3, name='Miniconf'),
            )
        self.log_in()

    def tearDown(self):
        self.log_out()
        model.submission.tables.submission_type.delete().execute()
        super(TestSubmission, self).tearDown()

    def test_selected_radio_button_in_edit(self):
        
        # Test that a radio button is checked when editing a submission
        s = Submission(id=1,
                       type=self.objectstore.get(SubmissionType, 3),
                       title='foo',
                       abstract='bar',
                       experience='',
                       url='')
        self.objectstore.save(s)
        
        self.p.submissions.append(s)
        
        self.objectstore.flush()

        resp = self.app.get(url_for(controller='submission',
                                    action='edit',
                                    id=s.id))

        print resp.session

        f = resp.form

        print "response:"
        print resp
        print "f.fields:"
        pprint.pprint(f.fields)

        # the value being returned is a string, from the form defaults
        self.assertEqual('3', f.fields['submission.type'][0].value)

        # clean up
        self.objectstore.delete(s)
        self.objectstore.flush()


    def test_submission_view_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = Person(email_address='test2@example.org',
                    password='test')
        self.objectstore.save(p2)
        # create a submission
        s = Submission(title='foo')
        self.objectstore.save(s)
        p2.submissions.append(s)
        self.objectstore.flush()
        # try to view the submission as the other person
        resp = self.app.get(url_for(controller='submission',
                                    action='view',
                                    id=s.id),
                            status=403)

        # clean up
        self.objectstore.delete(p2)
        self.objectstore.delete(s)
        self.objectstore.flush()


    def test_submission_edit_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = Person(email_address='test2@example.org',
                    password='test')
        self.objectstore.save(p2)
        # create a submission
        s = Submission(title='foo')
        self.objectstore.save(s)
        p2.submissions.append(s)
        self.objectstore.flush()
        # try to view the submission as the other person
        resp = self.app.get(url_for(controller='submission',
                                    action='edit',
                                    id=s.id),
                            status=403)

        # also try to post to it
        resp = self.app.post(url_for(controller='submission',
                                     action='edit',
                                     id=s.id),
                             params={},
                             status=403)

        # clean up
        self.objectstore.delete(p2)
        self.objectstore.delete(s)
        self.objectstore.flush()


    def test_submission_delete_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = Person(email_address='test2@example.org',
                    password='test')
        self.objectstore.save(p2)
        self.objectstore.flush()
        # create a submission
        s = Submission(title='foo')
        self.objectstore.save(s)
        p2.submissions.append(s)
        self.objectstore.flush()
        # try to view the submission as the other person
        resp = self.app.get(url_for(controller='submission',
                                    action='delete',
                                    id=s.id),
                            status=403)

        # also try to post to it
        resp = self.app.post(url_for(controller='submission',
                                     action='delete',
                                     id=s.id),
                             params={},
                             status=403)

        # clean up
        self.objectstore.delete(p2)
        self.objectstore.delete(s)
        self.objectstore.flush()


    def test_submission_list_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = Person(email_address='test2@example.org',
                    password='test')
        self.objectstore.save(p2)
        # create a submission
        s = Submission(title='foo')
        self.objectstore.save(s)
        p2.submissions.append(s)
        self.objectstore.flush()
        # try to view the submission as the other person
        resp = self.app.get(url_for(controller='submission',
                                    action='index'),
                            status=403)

        # clean up
        self.objectstore.delete(p2)
        self.objectstore.delete(s)
        self.objectstore.flush()


    def test_submit_another(self):
        # created guy with login
        # and a submission
        s1 = Submission(title='sub one')
        self.objectstore.save(s1)
        self.objectstore.flush()

        # now go home, click on the submit another link, and do so
        resp = self.app.get('/')
        print resp
        resp = resp.click(description='submit another')
        #print resp
        f = resp.form
        f['submission.title'] = 'sub two'
        f['submission.type'] = 1
        f['submission.abstract'] = "cubist"
        f['submission.experience'] = "n"
        print f.submit_fields()
        resp = f.submit()
        resp = resp.follow()

        # does it exist?
        subs = self.objectstore.query(Submission).select_by(title='sub two')
        self.assertEqual(1, len(subs))

        s2 = subs[0]
        # is it attached to our guy?
        self.failUnless(s2 in self.p.submissions, "s2 not in p.submissions (currently %r)" % self.p.submissions)
        
        # clean up
        self.objectstore.delete(s2)
        self.objectstore.delete(s1)
        self.objectstore.flush()
