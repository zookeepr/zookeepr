from zookeepr.tests.model import TableTest, model

class TestReviewTable(TableTest):
    table = model.proposal.tables.review
    samples = [dict(id=1,
                    proposal_id=1,
                    reviewer_id=1,
                    familiarity=0,
                    technical=1,
                    experience=1,
                    coolness=1,
                    stream_id=1,
                    comment="comment 1",
                    ),
               dict(id=2,
                    proposal_id=2,
                    reviewer_id=2,
                    familiarity=1,
                    technical=2,
                    experience=2,
                    coolness=2,
                    stream_id=2,
                    comment="comment 2",
                    ),
               ]
    not_nullable = ['proposal_id', 'reviewer_id']
                    
