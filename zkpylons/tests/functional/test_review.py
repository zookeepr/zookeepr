import pytest
from routes import url_for

from zk.model.review import Review

from .fixtures import StreamFactory, PersonFactory, ProposalFactory, RoleFactory, ProposalStatusFactory, ReviewFactory
from .utils import do_login


class TestReviewController(object):

    def test_create(self, app, db_session):

        StreamFactory(name='streamy')
        prop1 = ProposalFactory()
        prop2 = ProposalFactory()
        p = PersonFactory(roles=[RoleFactory(name='reviewer')])

        ProposalStatusFactory(name='Withdrawn') # Required by code


        db_session.commit()

        do_login(app, p)

        resp = app.get('/proposal/%d/review' % prop1.id)
        resp = resp.maybe_follow()
        f = resp.form
        f['review.score'] = -1
        f['review.comment'] = 'a'
        resp = f.submit()
        resp = resp.follow() # Failure indicates form validation error

        resp = app.get('/proposal/%d/review' % prop2.id)
        resp = resp.maybe_follow()
        f = resp.form
        f['review.score'] = 2
        f['review.comment'] = 'b'
        resp = f.submit()
        resp = resp.follow() # Failure indicates form validation error

        db_session.expunge_all()

        revs = Review.find_all()
        assert len(revs) == 2
        assert revs[0].score == -1
        assert revs[0].comment == 'a'
        assert revs[1].score == 2
        assert revs[1].comment == 'b'


    @pytest.mark.xfail # Test not yet written
    def test_review_feedback(self):
        """Test that one can put in optional feedback to the submitter from the review interface.
        """
        assert False

    @pytest.mark.xfail # Test not yet written
    def test_review_interface(self):
        """Test that the interface shows two lists, one of unreviewed proposals, and one of reviewed proposals"""
        assert False


    @pytest.mark.xfail # Test not yet written
    def test_review_interface_sorted(self):
        """Test that the reviewed proposals are sorted by rank"""
        assert False


    def test_reviews_not_isolated(self, app, db_session):
        """Test that a reviewer can see other reviews"""

        p1 = PersonFactory(roles=[RoleFactory(name='reviewer')], firstname="Scrouge")
        p2 = PersonFactory(firstname="Daffy")
        p3 = PersonFactory()
        prop = ProposalFactory(people=[p3])
        stream = StreamFactory()
        r1 = ReviewFactory(reviewer=p1, proposal=prop, score=-1, stream=stream)
        r2 = ReviewFactory(reviewer=p2, proposal=prop, score=2, stream=stream)
        ProposalStatusFactory(name='Withdrawn') # Required by code
        db_session.commit()

        do_login(app, p1)
        resp = app.get('/proposal/%d' % prop.id)

        # Page has list of reviews already set on proposal
        assert p1.firstname in unicode(resp.body, 'utf-8')
        assert p2.firstname in unicode(resp.body, 'utf-8')


    @pytest.mark.xfail # Test not yet written
    def test_reviewer_name_hidden_from_submitter(self):
        """Test taht a revier is anonymouse to submitters"""
        assert False


    @pytest.mark.xfail # Test not yet written
    def test_reviewer_cant_review_own_proposal(self):
        """Test that a reviewer can't review their own submissions."""
        assert False


    def test_only_one_review_per_reviewer_per_proposal(self, app, db_session):
        """test that reviewers can only do one review per proposal"""

        p1 = PersonFactory(roles=[RoleFactory(name='reviewer')])
        p2 = PersonFactory()
        prop = ProposalFactory(people=[p2])
        ProposalStatusFactory(name='Withdrawn') # Required by code
        db_session.commit()

        do_login(app, p1)
        resp = app.get('/proposal/%d/review' % prop.id)
        f = resp.form
        f['review.comment'] = 'first_review_comment'
        resp = f.submit()

        # do it again 
        f['review.comment'] = 'second_review_comment'
        resp = f.submit()
        resp = resp.follow() # Failure linked to errors in form submission

        # Old behaviour alerted that review had been performed
        # New behaviour is that we simply update with the second result

        db_session.expunge_all()

        revs = Review.find_all()
        assert len(revs) == 1
        assert revs[0].comment == "second_review_comment"

        
    def test_edit_review(self, app, db_session):
        """test that a reviewer can edit their review"""

        p1 = PersonFactory(roles=[RoleFactory(name='reviewer')])
        p2 = PersonFactory()
        prop = ProposalFactory(people=[p2])
        r = ReviewFactory(proposal=prop, reviewer=p1, score=-2, comment="It's a hard luck life")
        ProposalStatusFactory(name='Withdrawn') # Required by code
        db_session.commit()

        do_login(app, p1)
        resp = app.get(url_for(controller='review', action='edit', id=r.id))
        resp = resp.maybe_follow()
        assert r.comment in unicode(resp.body, 'utf-8')
        f = resp.form
        f['review.comment'] = 'hi!'
        f['review.score'] = 1
        resp = f.submit()
        resp = resp.follow()

        rid = r.id
        db_session.expunge_all()
        r2 = Review.find_by_id(rid)

        assert r2.comment == 'hi!'
        assert r2.score   == 1
