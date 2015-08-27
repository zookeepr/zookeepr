#from base_test import BaseTest

import pytest
import sys
import logging

from pyramid import testing
from sqlalchemy import create_engine
import zk.model.meta as meta
import zkpylons.model.meta as pymeta

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
    meta.engine = create_engine('postgresql://postgres@localhost/zktest')
    meta.Session.configure(bind=meta.engine)
    meta.Session.configure(autoflush=True)

    # Drop all data to establish known state
    meta.engine.execute("drop schema if exists public cascade")
    meta.engine.execute("create schema public")

    # Recreate tables
    meta.Base.metadata.create_all(meta.engine)

    # Also need to set zkpylons version of meta, hours of fun if you don't
    pymeta.engine = meta.engine
    pymeta.Session.configure(bind=meta.engine)
    pymeta.Session.configure(autoflush=True)

    # Run the actual test
    yield meta.Session

    # Throw away any DB changes that the test may have done
    meta.Session.rollback()
    meta.Session.close()
