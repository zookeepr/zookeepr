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
    def get(cls, key, category='general'):
        """ Get an entry from the config key store. """

        fetch = Session.query(cls).get((category, key))

        if (not fetch):
            log.warning("Config request for missing key: %s, %s", category, key)

        # Missing entries are returned as an empty string
        # This is the least obvious when directly exposed to the user
        return fetch.value if fetch else ""
