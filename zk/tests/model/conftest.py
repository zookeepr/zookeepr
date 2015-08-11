#from base_test import BaseTest

import pytest
import sys
import logging

from pyramid import testing
from sqlalchemy import create_engine
from zk.model.meta import Session, engine, Base

@pytest.yield_fixture
def app_config():
    config = testing.setUp()
    # Logging displayed by passing -s to pytest
    #logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    yield config
    testing.tearDown()

@pytest.yield_fixture
def db_session(app_config):
    # Set up SQLAlchemy to provide DB access
    # TODO: engine config should be from config file
    engine = create_engine('postgresql://zktest:zktest@localhost/zktest')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    # Run the actual test
    yield Session

    # Throw away any DB changes that the test may have done
    Session.rollback()
    Session.close()
