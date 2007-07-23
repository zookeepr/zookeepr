import pprint

from zookeepr.tests.functional import *

# class TestProposalBase(object):
#     """Base class that sets up proposal objects for experimenting with.
#     """
#     def setUp(self):
#         super(TestProposalBase, self).setUp()
        
#         self.proposal1 = model.Proposal(title='proposal1')
#         self.proposal2 = model.Proposal(title='proposal2')
#         self.dbsession.save(self.proposal1)
#         self.dbsession.save(self.proposal2)
#         self.dbsession.flush()

#     def tearDown(self):
#         self.dbsession.delete(self.proposal2)
#         self.dbsession.delete(self.proposal1)
#         self.dbsession.flush()
        
#         super(TestProposalBase, self).tearDown()

class TestProposal(SignedInCRUDControllerTest):
    model = model.Proposal
    name = 'proposal'
    url = '/proposal'
    samples = [dict(title='test',
                    abstract='abstract 1',
                    url='http://example.org',
                    ),
               dict(title='not a test',
                    abstract='abstract 2',
                    url='http://lca2007.linux.org.au',
                    ),
               ]

    def additional(self, obj):
        obj.people.append(self.person)
        obj.type = self.dbsession.query(model.ProposalType).get(1)
        return obj
    
    def setUp(self):
        super(TestProposal, self).setUp()
        model.proposal.tables.proposal_type.insert().execute(
            dict(id=1, name='Paper'),
            )
        model.proposal.tables.proposal_type.insert().execute(
            dict(id=2, name='Presentation'),
            )
        model.proposal.tables.proposal_type.insert().execute(
            dict(id=3, name='Miniconf'),
            )
        model.proposal.tables.assistance_type.insert().execute(
            dict(id=1, name='Need Assisatance'),
            )
        model.proposal.tables.assistance_type.insert().execute(
            dict(id=2, name='Don\'t Need Assistance'),
            )
        model.proposal.tables.assistance_type.insert().execute(
            dict(id=3, name='Don\'t Need Assistance maybe'),
            )
        model.proposal.tables.assistance_type.insert().execute(
            dict(id=4, name='Don\'t Need Assistance employer'),
            )

    def tearDown(self):
        model.proposal.tables.proposal_type.delete().execute()
        model.proposal.tables.assistance_type.delete().execute()
        super(TestProposal, self).tearDown()

    def test_selected_radio_button_in_edit(self):
        # Test that a radio button is checked when editing a proposal
        s = model.Proposal(id=1,
                       type=self.dbsession.get(model.ProposalType, 3),
                       title='foo',
                       abstract='bar',
                       url='')
        self.dbsession.save(s)
        
        self.person.proposals.append(s)
        
        self.dbsession.flush()

        resp = self.app.get(url_for(controller='proposal',
                                    action='edit',
                                    id=s.id))

        print resp.session

        f = resp.form

        print "response:"
        print resp
        print "f.fields:"
        pprint.pprint(f.fields)

        # the value being returned is a string, from the form defaults
        self.assertEqual('3', f.fields['proposal.type'][0].value)

        # clean up
        self.dbsession.delete(s)
        self.dbsession.flush()


    def test_proposal_view_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = model.Person(email_address='test2@example.org',
                    password='test',
		    handle='test')
        self.dbsession.save(p2)
        # create a proposal
        s = model.Proposal(title='foo')
        self.dbsession.save(s)
        p2.proposals.append(s)
        self.dbsession.flush()
        p2id = p2.id
        sid = s.id
        # try to view the proposal as the other person
        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=s.id),
                            status=403)

        # clean up
        self.dbsession.delete(self.dbsession.query(model.Person).get(p2id))
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(sid))
        self.dbsession.flush()


    def test_proposal_edit_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = model.Person(email_address='test2@example.org',
                    password='test',
		    handle='test')
        self.dbsession.save(p2)
        # create a proposal
        s = model.Proposal(title='foo')
        self.dbsession.save(s)
        p2.proposals.append(s)
        self.dbsession.flush()
        p2id = p2.id
        sid = s.id
        # try to view the proposal as the other person
        resp = self.app.get(url_for(controller='proposal',
                                    action='edit',
                                    id=sid),
                            status=403)

        # also try to post to it
        resp = self.app.post(url_for(controller='proposal',
                                     action='edit',
                                     id=sid),
                             params={},
                             status=403)

        # clean up
        self.dbsession.delete(self.dbsession.query(model.Person).get(p2id))
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(sid))
        self.dbsession.flush()


    def test_proposal_delete_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = model.Person(email_address='test2@example.org',
                    password='test',
		    handle='test')
        self.dbsession.save(p2)
        self.dbsession.flush()
        p2id = p2.id
        # create a proposal
        s = model.Proposal(title='foo')
        self.dbsession.save(s)
        p2.proposals.append(s)
        self.dbsession.flush()
        sid = s.id
        # try to view the proposal as the other person
        resp = self.app.get(url_for(controller='proposal',
                                    action='delete',
                                    id=sid),
                            status=403)

        # also try to post to it
        resp = self.app.post(url_for(controller='proposal',
                                     action='delete',
                                     id=sid),
                             params={},
                             status=403)

        # clean up
        self.dbsession.delete(self.dbsession.query(model.Person).get(p2id))
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(sid))
        self.dbsession.flush()


    def test_proposal_list_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = model.Person(email_address='test2@example.org',
                    password='test',
		    handle='test')
        self.dbsession.save(p2)
        # create a proposal
        s = model.Proposal(title='foo')
        self.dbsession.save(s)
        p2.proposals.append(s)
        self.dbsession.flush()
        p2id = p2.id
        sid = s.id
        # try to view the proposal as the other person
        resp = self.app.get(url_for(controller='proposal',
                                    action='index'),
                            status=403)

        # clean up
        self.dbsession.delete(self.dbsession.query(model.Person).get(p2id))
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(sid))
        self.dbsession.flush()


    def test_submit_another(self):
        # created guy with login
        # and a proposal
        s1 = model.Proposal(title='sub one')
        self.dbsession.save(s1)
        self.dbsession.flush()
        s1id = s1.id

        # now go home, click on the submit another link, and do so
        resp = self.app.get('/')
        print resp
        resp = resp.click(description='submit another')
        #print resp
        f = resp.form
        f['proposal.title'] = 'sub two'
        f['proposal.type'] = 1
        f['proposal.abstract'] = "cubist"
        f['person.experience'] = "n"
        f['attachment'] = "foo"
        print f.submit_fields()
        resp = f.submit()
        print resp
        resp = resp.follow()

        # does it exist?
        s2 = self.dbsession.query(model.Proposal).get_by(title='sub two')
        self.failIfEqual(None, s2)

        # is it attached to our guy?
        self.failUnless(s2 in self.person.proposals, "s2 not in p.proposals (currently %r)" % self.person.proposals)

        # do we have an attachment?
        self.failIfEqual([], s2.attachments)
        
        # clean up
        self.dbsession.delete(s2)
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(s1id))
        self.dbsession.flush()

    def test_proposal_list(self):
        # we're logged in but still can't see it
        resp = self.app.get(url_for(controller='proposal',
                                    action='index'),
                            status=403)

    def test_proposal_list_reviewer(self):
        # we're logged in and we're a reviewer
        r = model.Role('reviewer')
        self.person.roles.append(r)
        self.dbsession.save(r)
        self.dbsession.flush()

        self.failUnless('reviewer' in [x.name for x in self.person.roles])

        rid = r.id

        resp = self.app.get(url_for(controller='proposal',
                                    action='index'))


        # clean up
        self.dbsession.delete(self.dbsession.query(model.Role).get(rid))
        self.dbsession.flush()

    def test_proposal_view(self):
        p = model.Proposal(title='test view')
        self.dbsession.save(p)
        self.dbsession.flush()
        pid = p.id
        
        # we're logged in but this isn't our proposal..
        # should 403
        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=p.id),
                            status=403)
                            
        # clean up
        self.dbsession.delete(p)
        self.dbsession.flush()

    def test_proposal_view_ours(self):
        p = model.Proposal(title='test view',
                     abstract='abs',
                     type=self.dbsession.get(model.ProposalType, 3))
        self.dbsession.save(p)
        self.person.proposals.append(p)
        self.dbsession.flush()
        pid = p.id
        
        # we're logged in and this is ours
        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=pid))

        # clean up
        self.dbsession.delete(p)
        self.dbsession.flush()

    def test_proposal_view_as_reviewer(self):
        p = model.Proposal(title='test view',
                     abstract='abs',
                     type=self.dbsession.get(model.ProposalType, 3))
        self.dbsession.save(p)

        r = model.Role('reviewer')
        self.dbsession.save(r)
        self.person.roles.append(r)
        # need a stream
        s = model.Stream(name='stream')
        self.dbsession.save(s)
        self.dbsession.flush()
        pid = p.id
        rid = r.id
        sid = s.id
        self.dbsession.clear()
        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=p.id))
        # reviewers can review a proposal
        resp = resp.click('Review this proposal')

        # get the form and start reviewing!
        f = resp.form

        print f.fields

        f['review.score'] = 1
        f['review.stream'] = 1
        f['review.comment'] = "snuh"

        f.submit()

        # test that we have a review
        reviews = self.dbsession.query(model.Review).select()
        self.failIfEqual([], reviews)
        self.assertEqual(1, len(reviews))
        self.assertEqual("snuh", reviews[0].comment)
                                                            
        
        # clean up
        self.dbsession.delete(reviews[0])
        self.dbsession.delete(self.dbsession.query(model.Stream).get(sid))
        self.dbsession.delete(self.dbsession.query(model.Role).get(rid))
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(pid))
        self.dbsession.flush()


    def test_proposal_attach_more(self):
        p = model.Proposal(title='test view',
                     abstract='abs',
                     type=self.dbsession.query(model.ProposalType).get(3))
        self.dbsession.save(p)
        self.person.proposals.append(p)
        self.dbsession.flush()
        pid = p.id
        self.dbsession.clear()
        
        # we're logged in and this is ours
        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=pid))
        resp = resp.click('Add an attachment')

        f = resp.form
        f['attachment'] = "attachment"
        resp = f.submit()
        resp = resp.follow()

        atts = self.dbsession.query(model.Attachment).select()
        self.failIfEqual([], atts)
        self.assertEqual("attachment", str(atts[0].content))

        
        # clean up
        self.dbsession.delete(atts[0])
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(pid))
        self.dbsession.flush()


    def test_proposal_delete_attachment(self):
        p = model.Proposal(title='test view',
                     abstract='abs',
                     type=self.dbsession.query(model.ProposalType).get(3))
        self.dbsession.save(p)
        self.person.proposals.append(p)
        a = model.Attachment(content="foo")
        self.dbsession.save(a)
        p.attachments.append(a)
        self.dbsession.flush()
        pid = p.id
        aid = a.id
        self.dbsession.clear()
        
        # we're logged in and this is ours
        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=pid))
        resp = resp.click('delete')

        print resp.request.url
        f = resp.form
        print f.fields
        resp = f.submit()

        resp = resp.follow()

        atts = self.dbsession.query(model.Attachment).select()
        self.assertEqual([], atts)

        
        self.assertEqual(url_for(controller='proposal',
                                 action='view',
                                 id=pid),
                         resp.request.url)

        # clean up
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(pid))
        self.dbsession.flush()

