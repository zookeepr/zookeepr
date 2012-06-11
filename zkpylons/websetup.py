"""Setup the zkpylons application"""
import logging

from zkpylons.config.environment import load_environment
from zkpylons.model import meta

import zkpylons.model

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup zkpylons here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    log.info("Creating tables...")
    meta.metadata.create_all(bind=meta.engine)

    log.info("Populating tables...")
    zkpylons.model.setup(meta)

    log.info("Successfully set up.")


