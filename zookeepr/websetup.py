"""Setup the zookeepr application"""
import logging

from zookeepr.config.environment import load_environment
from zookeepr.model import meta

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup zookeepr here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    log.info("Creating tables...")
    meta.metadata.create_all(bind=meta.engine)
    log.info("Successfully set up.")

    #log.info("Populating tables...")
    #page = model.Page(
    #        title=u'FrontPage',
    #        content=u'**Welcome** to the QuickWiki front page!'
    #)
    #meta.Session.add(page)
    #meta.Session.commit()

    log.info("Successfully set up.")


