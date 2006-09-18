import pprint

from zookeepr.model import Proposal, ProposalType, Person, Attachment
from zookeepr.tests.functional import *

class TestProposalBase(object):
    """Base class that sets up proposal objects for experimenting with.
    """
    def setUp(self):
        super(TestProposalBase, self).setUp()
        
        self.proposal1 = model.Proposal(title='proposal1')
        self.proposal2 = model.Proposal(title='proposal2')
        objectstore.save(self.proposal1)
        objectstore.save(self.proposal2)
        objectstore.flush()

    def tearDown(self):
        objectstore.delete(self.proposal2)
        objectstore.delete(self.proposal1)
        objectstore.flush()
        
        super(TestProposalBase, self).tearDown()

class TestProposal(SignedInControllerTest):
    model = Proposal
    name = 'proposal'
    url = '/proposal'
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
        obj.people.append(self.person)
        obj.type = objectstore.get(ProposalType, 1)
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

    def tearDown(self):
        model.proposal.tables.proposal_type.delete().execute()
        super(TestProposal, self).tearDown()

    def test_selected_radio_button_in_edit(self):
        # Test that a radio button is checked when editing a proposal
        s = Proposal(id=1,
                       type=objectstore.get(ProposalType, 3),
                       title='foo',
                       abstract='bar',
                       experience='',
                       url='')
        objectstore.save(s)
        
        self.person.proposals.append(s)
        
        objectstore.flush()

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
        objectstore.delete(s)
        objectstore.flush()


    def test_proposal_view_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = Person(email_address='test2@example.org',
                    password='test')
        objectstore.save(p2)
        # create a proposal
        s = Proposal(title='foo')
        objectstore.save(s)
        p2.proposals.append(s)
        objectstore.flush()
        # try to view the proposal as the other person
        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=s.id),
                            status=403)

        # clean up
        objectstore.delete(p2)
        objectstore.delete(s)
        objectstore.flush()


    def test_proposal_edit_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = Person(email_address='test2@example.org',
                    password='test')
        objectstore.save(p2)
        # create a proposal
        s = Proposal(title='foo')
        objectstore.save(s)
        p2.proposals.append(s)
        objectstore.flush()
        # try to view the proposal as the other person
        resp = self.app.get(url_for(controller='proposal',
                                    action='edit',
                                    id=s.id),
                            status=403)

        # also try to post to it
        resp = self.app.post(url_for(controller='proposal',
                                     action='edit',
                                     id=s.id),
                             params={},
                             status=403)

        # clean up
        objectstore.delete(p2)
        objectstore.delete(s)
        objectstore.flush()


    def test_proposal_delete_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = Person(email_address='test2@example.org',
                    password='test')
        objectstore.save(p2)
        objectstore.flush()
        # create a proposal
        s = Proposal(title='foo')
        objectstore.save(s)
        p2.proposals.append(s)
        objectstore.flush()
        # try to view the proposal as the other person
        resp = self.app.get(url_for(controller='proposal',
                                    action='delete',
                                    id=s.id),
                            status=403)

        # also try to post to it
        resp = self.app.post(url_for(controller='proposal',
                                     action='delete',
                                     id=s.id),
                             params={},
                             status=403)

        # clean up
        objectstore.delete(p2)
        objectstore.delete(s)
        objectstore.flush()


    def test_proposal_list_lockdown(self):
        # we got one person already with login
        # create a sceond
        p2 = Person(email_address='test2@example.org',
                    password='test')
        objectstore.save(p2)
        # create a proposal
        s = Proposal(title='foo')
        objectstore.save(s)
        p2.proposals.append(s)
        objectstore.flush()
        # try to view the proposal as the other person
        resp = self.app.get(url_for(controller='proposal',
                                    action='index'),
                            status=403)

        # clean up
        objectstore.delete(p2)
        objectstore.delete(s)
        objectstore.flush()


    def test_submit_another(self):
        # created guy with login
        # and a proposal
        s1 = Proposal(title='sub one')
        objectstore.save(s1)
        objectstore.flush()

        # now go home, click on the submit another link, and do so
        resp = self.app.get('/')
        print resp
        resp = resp.click(description='submit another')
        #print resp
        f = resp.form
        f['proposal.title'] = 'sub two'
        f['proposal.type'] = 1
        f['proposal.abstract'] = "cubist"
        f['proposal.experience'] = "n"
        f['attachment'] = "foo"
        print f.submit_fields()
        resp = f.submit()
        resp = resp.follow()

        # does it exist?
        subs = objectstore.query(Proposal).select_by(title='sub two')
        self.assertEqual(1, len(subs))

        s2 = subs[0]
        # is it attached to our guy?
        self.failUnless(s2 in self.person.proposals, "s2 not in p.proposals (currently %r)" % self.person.proposals)

        # do we have an attachment?
        self.failIfEqual([], subs[0].attachments)
        
        # clean up
        objectstore.delete(s2)
        objectstore.delete(s1)
        objectstore.flush()

    def test_proposal_list(self):
        # we're logged in but still can't see it
        resp = self.app.get(url_for(controller='proposal',
                                    action='index'),
                            status=403)

    def test_proposal_list_reviewer(self):
        # we're logged in and we're a reviewer
        r = model.Role('reviewer')
        self.person.roles.append(r)
        objectstore.save(r)
        objectstore.flush()

        resp = self.app.get(url_for(controller='proposal',
                                    action='index'))


        # clean up
        objectstore.delete(r)
        objectstore.flush()

    def test_proposal_view(self):
        p = Proposal(title='test view')
        objectstore.save(p)
        objectstore.flush()
        pid = p.id
        
        # we're logged in but this isn't our proposal..
        # should 403
        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=p.id),
                            status=403)
                            
        # clean up
        objectstore.delete(objectstore.get(Proposal, pid))
        objectstore.flush()

    def test_proposal_view_ours(self):
        p = Proposal(title='test view',
                     abstract='abs',
                     type=objectstore.get(ProposalType, 3))
        objectstore.save(p)
        self.person.proposals.append(p)
        objectstore.flush()
        pid = p.id
        objectstore.clear()
        
        # we're logged in and this is ours
        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=pid))

        # clean up
        objectstore.delete(objectstore.get(Proposal, pid))
        objectstore.flush()

    def test_proposal_view_as_reviewer(self):
        p = Proposal(title='test view',
                     abstract='abs',
                     experience='snuh',
                     type=objectstore.get(ProposalType, 3))
        objectstore.save(p)

        r = model.Role('reviewer')
        objectstore.save(r)
        self.person.roles.append(r)
        # need a stream
        s = model.Stream(name='stream')
        objectstore.save(s)
        objectstore.flush()
        pid = p.id
        rid = r.id
        sid = s.id
        objectstore.clear()

        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=p.id))
        # reviewers can review a proposal
        resp = resp.click('Review this proposal')

        # get the form and start reviewing!
        f = resp.form

        print f.fields

        f['review.familiarity'] = 1
        f['review.technical'] = 1
        f['review.experience'] = 1
        f['review.coolness'] = 1
        f['review.stream'] = 1
        f['review.comment'] = "snuh"

        f.submit()

        # test that we have a review
        reviews = objectstore.query(model.Review).select()
        self.assertEqual(1, len(reviews))
        self.assertEqual("snuh", reviews[0].comment)
                                                            
        
        # clean up
        objectstore.delete(objectstore.get(model.Review, reviews[0].id))
        objectstore.delete(objectstore.get(model.Stream, sid))
        objectstore.delete(objectstore.get(model.Role, rid))
        objectstore.delete(objectstore.get(Proposal, pid))
        objectstore.flush()


    def test_proposal_attach_more(self):
        p = Proposal(title='test view',
                     abstract='abs',
                     type=objectstore.get(ProposalType, 3))
        objectstore.save(p)
        self.person.proposals.append(p)
        objectstore.flush()
        pid = p.id
        objectstore.clear()
        
        # we're logged in and this is ours
        resp = self.app.get(url_for(controller='proposal',
                                    action='view',
                                    id=pid))
        resp = resp.click('Add an attachment')

        f = resp.form
        f['attachment'] = "attachment"
        resp = f.submit()
        resp = resp.follow()

        atts = objectstore.query(Attachment).select()
        self.failIfEqual([], atts)
        self.assertEqual("attachment", str(atts[0].content))

        
        # clean up
        objectstore.delete(atts[0])
        objectstore.delete(objectstore.get(Proposal, pid))
        objectstore.flush()


    def test_proposal_delete_attachment(self):
        p = Proposal(title='test view',
                     abstract='abs',
                     type=objectstore.get(ProposalType, 3))
        objectstore.save(p)
        self.person.proposals.append(p)
        a = Attachment(content="foo")
        objectstore.save(a)
        p.attachments.append(a)
        objectstore.flush()
        pid = p.id
        aid = a.id
        objectstore.clear()
        
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

        atts = objectstore.query(Attachment).select()
        self.assertEqual([], atts)

        
        self.assertEqual(url_for(controller='proposal',
                                 action='view',
                                 id=pid),
                         resp.request.url)

        # clean up
        objectstore.delete(objectstore.get(Proposal, pid))
        objectstore.flush()

