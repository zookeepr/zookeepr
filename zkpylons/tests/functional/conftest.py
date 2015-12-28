import pytest
import sys
import logging

from sqlalchemy import create_engine
import zk.model.meta as zkmeta
import zkpylons.model.meta as pymeta

from zkpylons.config.routing import make_map

from paste.deploy import loadapp
from webtest import TestApp

from paste.fixture import Dummy_smtplib

from .fixtures import ConfigFactory

from ConfigParser import ConfigParser

# Get settings from config file, only need it once
ini = ConfigParser()
ini_filename = "test.ini"
ini.read(ini_filename)

# Logging displayed by passing -s to pytest
#logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

@pytest.yield_fixture
def map():
    config = {
        'pylons.paths' : { 'controllers' : None },
        'debug' : True,
    }
    yield make_map(config)

@pytest.yield_fixture
def app():
    wsgiapp = loadapp('config:'+ini_filename, relative_to=".")
    app = TestApp(wsgiapp)
    yield app

class DoubleSession(object):
    # There is an issue with the zkpylons -> zk migration
    # Some files use zk.model, which uses zk.model.meta.Session
    # Some files use zkpylons.model, which uses zkpylons.model.meta.Session
    # Some files use relative paths, which means you can kinda guess at it
    # The best way around this is to configure both Session objects
    # But then operations frequently have to be applied to both
    # This class wraps operations needed for testing, and applies both

    def __init__(self, session1, session2):
        self.s1 = session1
        self.s2 = session2

    def remove(self):
        self.s1.remove()
        self.s2.remove()

    def configure(self, engine):
        self.s1.configure(bind=engine)
        self.s2.configure(bind=engine)
        self.s1.configure(autoflush=False)
        self.s2.configure(autoflush=False)


    def commit(self):
        self.s1.commit()
        self.s2.commit()

    # TODO: Maybe expire_all or refresh would be better
    def expunge_all(self):
        self.s1.expunge_all()
        self.s2.expunge_all()

    def query(self, cls):
        return self.s1.query(cls)

    def execute(self, *args, **kwargs):
        return self.s1.execute(*args, **kwargs)

base_general_config = {
        'sponsors'          : {"top":[],"slideshow":[]},
        'account_creation'  : True,
        'cfp_status'        : "open",
        'conference_status' : "open",
        }

base_rego_config = {
        'personal_info' : {"phone":"yes","home_address":"yes"}
        }

@pytest.yield_fixture
def db_session():
    # Set up SQLAlchemy to provide DB access
    dsess = DoubleSession(zkmeta.Session, pymeta.Session)

    # Clean up old sessions if they exist
    dsess.remove()

    engine = create_engine(ini.get("app:main", "sqlalchemy.url"))

    # Drop all data to establish known state, mostly to prevent primary-key conflicts
    engine.execute("drop schema if exists public cascade")
    engine.execute("create schema public")

    zkmeta.Base.metadata.create_all(engine)

    dsess.configure(engine)

    # Create basic config values, to allow basic pages to render
    for key, val in base_general_config.iteritems():
        ConfigFactory(key=key, value=val)
    for key, val in base_rego_config.iteritems():
        ConfigFactory(category='rego', key=key, value=val)
    dsess.commit()

    # Run the actual test
    yield dsess

    # No rollback, for functional tests we have to actually commit to DB


@pytest.yield_fixture
def smtplib():
    Dummy_smtplib.install()

    yield Dummy_smtplib

    if Dummy_smtplib.existing:
        Dummy_smtplib.existing.reset()

