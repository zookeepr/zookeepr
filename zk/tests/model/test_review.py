# pytest magic: from .conftest import app_config, db_session

from .fixtures import ReviewFactory, ProposalFactory, StreamFactory, PersonFactory
from zk.model.review import Review

import pytest

class TestReviewModel(object):
    def test_one_review_per_reviewer_per_proposal(self, db_session):
        """Test that reviewers can only review each proposal once"""
        proposal = ProposalFactory()
        stream = StreamFactory()
        reviewer = PersonFactory()
        db_session.flush()

        # create a review
        review1 = ReviewFactory(reviewer=reviewer, score=1, stream=stream, proposal=proposal)
        db_session.flush()

        # create a second, identical
        review2 = ReviewFactory(reviewer=reviewer, score=1, stream=stream, proposal=proposal)
        # raise an exception when trying to commit this
        with pytest.raises(Exception):
            db_session.flush()
