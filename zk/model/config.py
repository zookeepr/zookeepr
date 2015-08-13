""" Configuration key store, elements such as event_city or contact_email """
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON # Required - unsure why
from meta import Session, Base

import logging
log = logging.getLogger(__name__)

class Config(Base):
    __tablename__ = 'config'
    category    = sa.Column(sa.types.String, primary_key=True)
    key         = sa.Column(sa.types.String, primary_key=True)
    value       = sa.Column(sa.dialects.postgresql.JSON)
    description = sa.Column(sa.types.String)
    # NOTE: Non-postgresql requires the use of a decorator

    default_category = 'general'

    @classmethod
    def get(cls, key, category=default_category):
        """ Get an entry from the config key store. """

        fetch = Session.query(cls).get((category, key))

        if (not fetch):
            log.warning("Config request for missing key: %s, %s", category, key)

        # Missing entries are returned as an empty string
        # This is the least obvious when directly exposed to the user
        return fetch.value if fetch else ""

    @classmethod
    def find_all(cls):
        return Session.query(cls).order_by(cls.category, cls.key).all()

    @classmethod
    def find_by_pk(cls, pk):
        return Session.query(cls).get(pk)

    @classmethod
    def find_by_category(cls, category):
        return Session.query(cls).filter(cls.category == category).all()
