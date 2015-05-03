""" Configuration key store, elements such as event_city or contact_email """
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import JSON # Required - unsure why
from meta import Base, Session, metadata

import logging
log = logging.getLogger(__name__)

class Config(Base):
    __tablename__ = 'config'
    category = sa.Column(sa.types.String, primary_key=True)
    key      = sa.Column(sa.types.String, primary_key=True)
    value    = sa.Column(sa.dialects.postgresql.JSON)
    # NOTE: Non-postgresql requires the use of a decorator

    @classmethod
    def get(cls, category, key=None):
        """ Get an entry from the config key store

        Calling form:
        get(category, key) - Fetches the specified value from the database
        get(key) - Fetches the value from the database with the general category
        """

        if key is None:
            key = category
            category = 'general'

        fetch = Session.query(cls).get((category, key))

        if (not fetch):
            log.info("Config request for missing key: %s, %s", category, key)

        # Missing entries are returned as an empty string
        # This is the least obvious when directly exposed to the user
        return fetch.value if fetch else ""
