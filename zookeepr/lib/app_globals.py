import os

import pylons.middleware
import sqlalchemy

import zookeepr.models as model
from zookeepr.lib.auth import UserModelAuthStore

class Globals(pylons.middleware.Globals):

    def __init__(self, global_conf, app_conf, **extra):
        """
        You can put any objects which need to be initialised only once
        here as class attributes and they will be available as globals
        everywhere in your application and will be intialised only once,
        not on every request.
        
        ``global_conf``
            The same as variable used throughout ``config/middleware.py``
            namely, the variables from the ``[DEFAULT]`` section of the
            configuration file.
            
        ``app_conf``
            The same as the ``kw`` dictionary used throughout 
            ``config/middleware.py`` namely, the variables the section 
            in the config file for your application.
            
        ``extra``
            The configuration returned from ``load_config`` in 
            ``config/middleware.py`` which may be of use in the setup of 
            your global variables.
            
        """
        sqlalchemy.global_connect(app_conf['dburi'])

        # FIXME: this method for creating the tables if the databsae was just created is not very
        # robust; currently it's trapping an exception created by pysqlite2
        # or a postgresql one
        try:
            model.person.create()
            model.submission_type.create()
            model.submission.create()
        except sqlalchemy.SQLError, e:
            # we only want to pass on operational errors
            if e.args[0].find('table person already exists') == -1 or \
               e.args[0].find("Relation 'person_id_seq' already exists") == 1:
                raise e


        self.auth = UserModelAuthStore()

    def __del__(self):
        """
        Put any cleanup code to be run when the application finally exits 
        here.
        """
        pass
