import pytest
from routes import url_for

from zk.model.attachment import Attachment
from zk.model.proposal import Proposal, ProposalType
from zk.model.person import Person
from zk.model.review import Review

from webtest.forms import Upload

from .fixtures import PersonFactory, ProposalFactory, AttachmentFactory, RoleFactory, StreamFactory, ProposalStatusFactory, ProposalTypeFactory, TravelAssistanceTypeFactory, AccommodationAssistanceTypeFactory, TargetAudienceFactory
from .utils import do_login

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
        pers = PersonFactory(
                # Set detail to avoid incomplete profile flag
                firstname = 'Testguy',
                lastname  = 'Testguy',
                i_agree   = True,
                activated = True,
                address1  = 'Somewhere',
                city      = 'Over the rainbow',
                postcode  = 'Way up high',
                )
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


@pytest.mark.xfail # TODO: Need a way to set cfp_status at run time
class TestCFPStates(object):

    def test_not_open(self, app):
        lca_info['cfp_status'] = 'not_open'
        resp = app.get('/programme/submit_a_proposal')
        assert "is not open!" in unicode(resp.body, 'utf-8')

    def test_open(self, app):
        lca_info['cfp_status'] = 'open'
        resp = app.get('/programme/submit_a_proposal')
        assert "is open!" in unicode(resp.body, 'utf-8')

    def test_closed(self, app):
        lca_info['cfp_status'] = 'open'
        resp = app.get('/programme/submit_a_proposal')
        assert "is closed!" in unicode(resp.body, 'utf-8')
