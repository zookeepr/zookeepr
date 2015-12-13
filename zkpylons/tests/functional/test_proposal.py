from routes import url_for

from zk.model.attachment import Attachment
from zk.model.proposal import Proposal, ProposalType
from zk.model.person import Person
from zk.model.review import Review

from webtest.forms import Upload

from .fixtures import PersonFactory, ProposalFactory, AttachmentFactory, RoleFactory, StreamFactory, ProposalStatusFactory, ProposalTypeFactory, TravelAssistanceTypeFactory, AccommodationAssistanceTypeFactory, TargetAudienceFactory, ConfigFactory, CompletePersonFactory
from .utils import do_login, isSignedIn

class TestProposal(object):

    def test_proposal_view_lockdown(self, app, db_session):
        prop = ProposalFactory()
        pers1 = PersonFactory(proposals = [prop])
        pers2 = PersonFactory()
        db_session.commit()

        # try to view the proposal as the other person
        do_login(app, pers2)
        resp = app.get(url_for(controller='proposal', action='edit', id=prop.id), status=403)
        resp = app.get(url_for(controller='proposal', action='view', id=prop.id), status=403)


    def test_proposal_edit_lockdown(self, app, db_session):
        prop = ProposalFactory()
        pers1 = PersonFactory(proposals = [prop])
        pers2 = PersonFactory()
        db_session.commit()

        # try to edit the proposal as the other person
        do_login(app, pers2)
        resp = app.get(url_for(controller='proposal', action='edit', id=prop.id), status=403)
        resp = app.post(url_for(controller='proposal', action='edit', id=prop.id), params={}, status=403)


    def test_proposal_withdraw_lockdown(self, app, db_session):
        prop = ProposalFactory()
        pers1 = PersonFactory(proposals = [prop])
        pers2 = PersonFactory()
        db_session.commit()

        # try to delete the proposal as the other person
        do_login(app, pers2)
        resp = app.get(url_for(controller='proposal', action='withdraw', id=prop.id), status=403)
        resp = app.post(url_for(controller='proposal', action='withdraw', id=prop.id), params={}, status=403)

    def test_proposal_list_lockdown(self, app, db_session):
        prop = ProposalFactory()
        pers1 = PersonFactory(proposals = [prop])
        pers2 = PersonFactory()
        db_session.commit()

        # try to view the proposal as the other person
        do_login(app, pers2)
        resp = app.get(url_for(controller='proposal', action='index'))
        assert prop.title not in unicode(resp.body, 'utf-8')
        assert "You haven't submitted any proposals" in unicode(resp.body, 'utf-8')

    def test_submit_another(self, app, db_session, smtplib):
        # created guy and proposal
        pers = CompletePersonFactory()
        prop = ProposalFactory(title='sub one', people=[pers])
        type = ProposalTypeFactory()
        stat = ProposalStatusFactory(name = 'Pending Review') # Required by code
        trav = TravelAssistanceTypeFactory()
        accm = AccommodationAssistanceTypeFactory()
        audc = TargetAudienceFactory()
        db_session.commit()

        # now go to list, click on the submit another link, and do so
        do_login(app, pers)
        resp = app.get(url_for(controller='proposal', action='index'))
        assert prop.title in unicode(resp.body, 'utf-8')
        assert "You haven't submitted any proposals" not in unicode(resp.body, 'utf-8')

        resp = resp.click(description='New proposal')
        resp = resp.maybe_follow()
        f = resp.form
        f['proposal.title']    = 'sub two'
        f['proposal.type']     = str(type.id)
        f['proposal.abstract'] = "cubist"
        f['proposal.accommodation_assistance'] = str(accm.id)
        f['proposal.travel_assistance'] = str(trav.id)
        f['proposal.audience'] = str(audc.id)
        f['person.experience'] = "n"
        f['attachment']        = "foo"
        f['person.mobile']     = "NONE"
        f['person.bio']        = "Jim isn't real Dave, he never was"
        resp = f.submit()
        resp.status_code = 302 # Failure suggests form didn't submit cleanly

        pers_id = pers.id
        db_session.expunge_all()

        # does it exist?
        s2 = Proposal.find_by_title('sub two')
        assert len(s2) == 1
        s2 = s2[0]
        assert Person.find_by_id(pers_id) in s2.people # Attached to correct person
        assert len(s2.attachments) == 1 # With attachment

        # Ensure that confirmation email was sent
        assert smtplib.existing is not None
        assert "Thank you for proposing" in smtplib.existing.message

    def test_proposal_list_normals_denied(self, app, db_session):
        pers = PersonFactory()
        prop = ProposalFactory()
        ProposalStatusFactory(name='Withdrawn') # Required by code
        db_session.commit()

        # we're logged in but still can't see it
        do_login(app, pers)
        resp = app.get(url_for(controller='proposal', action='review_index'), status=403)

    def test_proposal_list_reviewer(self, app, db_session):
        role = RoleFactory(name = 'reviewer')
        pers = PersonFactory(roles = [role])
        prop = ProposalFactory()
        ProposalStatusFactory(name='Withdrawn') # Required by code
        db_session.commit()

        # we're logged in and we're a reviewer
        do_login(app, pers)
        resp = app.get(url_for(controller='proposal', action='review_index'))

    def test_proposal_view(self, app, db_session):
        pers = PersonFactory()
        prop = ProposalFactory()
        db_session.commit()
        
        # we're logged in but this isn't our proposal..
        # should 403
        do_login(app, pers)
        resp = app.get(url_for(controller='proposal', action='view', id=prop.id), status=403)
                            
    def test_proposal_view_ours(self, app, db_session):
        prop = ProposalFactory()
        pers = PersonFactory(proposals = [prop])
        db_session.commit()
        
        # we're logged in and this is ours
        do_login(app, pers)
        resp = app.get(url_for(controller='proposal', action='view', id=prop.id))

    def test_proposal_view_as_reviewer(self, app, db_session):
        prop = ProposalFactory()
        role = RoleFactory(name = 'reviewer')
        pers = PersonFactory(roles = [role])
        strm = StreamFactory() # need a stream
        ProposalStatusFactory(name='Withdrawn') # Required by code
        db_session.commit()

        do_login(app, pers)

        # reviewers can review a proposal
        resp = app.get(url_for(controller='proposal', action='view', id=prop.id))
        resp = resp.click('Review this proposal', index=0)

        # get the form and start reviewing!
        f = resp.form
        f['review.score'] = 1
        f['review.stream'] = strm.id
        f['review.comment'] = "snuh"
        f.submit()

        db_session.expunge_all()

        # test that we have a review
        reviews = Review.find_all()
        assert len(reviews) == 1
        assert reviews[0].comment == "snuh"
                                                            
        
    def test_proposal_attach_more(self, app, db_session):
        pers = PersonFactory()
        prop = ProposalFactory(people = [pers])
        ProposalStatusFactory(name='Withdrawn') # Required by code
        db_session.commit()
        
        # we're logged in and this is ours
        do_login(app, pers)
        resp = app.get(url_for(controller='proposal', action='view', id=prop.id))
        resp = resp.click('Add an attachment')

        f = resp.form
        f['attachment'] = Upload("test.ini")
        resp = f.submit()
        resp = resp.follow()

        db_session.expunge_all()

        atts = Attachment.find_all();
        assert len(atts) == 1
        assert '[app:main]' in atts[0].content

        
    def test_proposal_delete_attachment(self, app, db_session):
        pers = PersonFactory()
        prop = ProposalFactory()
        pers.proposals.append(prop)
        atta = AttachmentFactory(proposal=prop)
        db_session.commit()
        
        # we're logged in and this is ours
        do_login(app, pers)
        resp = app.get(url_for(controller='proposal', action='view', id=prop.id))
        resp = resp.click('delete')

        f = resp.form
        resp = f.submit()

        resp = resp.follow()

        assert resp.request.path == url_for(controller='proposal', action='view', id=prop.id)

        db_session.expunge_all()

        atts = Attachment.find_all();
        assert atts == []

from zk.model.config import Config

class TestCFPStates(object):

    def test_not_open(self, app, db_session):
        # Entry created by init, update it
        Config.find_by_pk(('general','cfp_status')).value = 'not_open'
        pers = CompletePersonFactory()
        db_session.commit()

        resp = do_login(app, pers)
        resp = app.get('/programme/submit_a_proposal')
        assert "The call for proposals has not opened yet" in unicode(resp.body, 'utf-8')

    def test_open(self, app, db_session):
        # Entry created by init, update it
        Config.find_by_pk(('general','cfp_status')).value = 'open'
        pers = CompletePersonFactory()
        db_session.commit()

        resp = do_login(app, pers)
        resp = app.get('/programme/submit_a_proposal')
        assert "The name of your proposal" in unicode(resp.body, 'utf-8')

    def test_closed(self, app, db_session):
        # Entry created by init, update it
        Config.find_by_pk(('general','cfp_status')).value = 'closed'
        pers = CompletePersonFactory()
        db_session.commit()

        resp = do_login(app, pers)
        resp = app.get('/programme/submit_a_proposal')
        assert "The call for proposals is now closed" in unicode(resp.body, 'utf-8')

class TestAttachment(object):

    def test_permissions(self, app, db_session):
        pers = PersonFactory()
        sec_pers = PersonFactory()
        rev_pers = PersonFactory(roles = [RoleFactory(name = 'reviewer')])
        org_pers = PersonFactory(roles = [RoleFactory(name = 'organiser')])
        other_pers = PersonFactory()
        ProposalStatusFactory(name='Withdrawn') # Required by code
        # Multiple attachments for deletion testing
        prop = ProposalFactory(people = [pers, sec_pers])
        att1 = AttachmentFactory(proposal=prop)
        att2 = AttachmentFactory(proposal=prop)
        att3 = AttachmentFactory(proposal=prop)
        att4 = AttachmentFactory(proposal=prop)
        db_session.commit()
        
        # we're logged in and this is ours
        do_login(app, pers)
        resp = app.get(url_for(controller='attachment', action='view', id=att1.id))
        assert resp.content_type == "application/octet-stream"
        resp = app.get(url_for(controller='attachment', action='delete', id=att1.id))
        assert "Are you sure you want to delete this attachment" in unicode(resp.body, 'utf-8')
        resp = app.post(url_for(controller='attachment', action='delete', id=att1.id), status=302)

        # this is also ours
        do_login(app, sec_pers)
        resp = app.get(url_for(controller='attachment', action='view', id=att2.id))
        assert resp.content_type == "application/octet-stream"
        resp = app.get(url_for(controller='attachment', action='delete', id=att2.id))
        assert "Are you sure you want to delete this attachment" in unicode(resp.body, 'utf-8')
        resp = app.post(url_for(controller='attachment', action='delete', id=att2.id), status=302)

        # we're organiser/admin
        do_login(app, org_pers)
        resp = app.get(url_for(controller='attachment', action='view', id=att3.id))
        assert resp.content_type == "application/octet-stream"
        resp = app.get(url_for(controller='attachment', action='delete', id=att3.id))
        assert "Are you sure you want to delete this attachment" in unicode(resp.body, 'utf-8')
        resp = app.post(url_for(controller='attachment', action='delete', id=att3.id), status=302)

        # we're a reviewer
        do_login(app, rev_pers)
        resp = app.get(url_for(controller='attachment', action='view', id=att4.id), status=403)
        assert resp.content_type == "text/html"
        resp = app.get(url_for(controller='attachment', action='delete', id=att4.id), status=403)
        resp = app.post(url_for(controller='attachment', action='delete', id=att4.id), status=403)

        # we're logged in and this isn't ours
        do_login(app, other_pers)
        resp = app.get(url_for(controller='attachment', action='view', id=att4.id), status=403)
        assert resp.content_type == "text/html"
        resp = app.get(url_for(controller='attachment', action='delete', id=att4.id), status=403)
        resp = app.post(url_for(controller='attachment', action='delete', id=att4.id), status=403)

        # we're not logged in
        app.get('/person/signout')
        assert not isSignedIn(app)
        resp = app.get(url_for(controller='attachment', action='view', id=att4.id))#, status=404)
        assert resp.content_type == "text/html"
        assert "User doesn't have any of the specified roles" in unicode(resp.body, 'utf-8')
        resp = app.get(url_for(controller='attachment', action='delete', id=att4.id))
        assert "Don't have an account?" in unicode(resp.body, 'utf-8')
        resp = app.post(url_for(controller='attachment', action='delete', id=att4.id))
        assert "Don't have an account?" in unicode(resp.body, 'utf-8')

        db_session.expunge_all()
        atts = Attachment.find_all();
        assert len(atts) == 1
        assert atts[0].id == att4.id
