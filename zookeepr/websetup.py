import os

from paste.deploy import appconfig
import sqlalchemy

from lib.app_globals import Globals

def setup_config(command, filename, section, vars):
    """Place any commands to set up zookeepr here.
    """

    # The connection to the AuthKit store is made in ``app_globals.py`` but
    # that doesn't mean the necessary tables, users, roles, etc have been
    # set up.  We set them up here.
    #config_spec = 'config:' + filename
    #app = appconfig(config_spec, relative_to=os.getcwd())
    #g = Globals({}, app)
    #g.auth.create_store()
    #g.auth.add_user('jaq', password='bananas')

    
    #r = model.Person(handle='root', password='root', email_address='')
    #a = model.Role('admin')
    #r.roles.append(a)
    #sqlalchemy.objectstore.flush()
