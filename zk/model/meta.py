"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['Session', 'engine', 'metadata', 'Base']

# SQLAlchemy database engine. Updated by model.init_model()
engine = None

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker(autocommit=False))

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database

metadata = MetaData()
Base = declarative_base(metadata=metadata)

@classmethod
def query(cls):
    return Session.query(cls).order_by(id)

Base.query = query
