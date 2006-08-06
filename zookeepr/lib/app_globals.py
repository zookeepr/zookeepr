import os

from zookeepr import model
from sqlalchemy import global_connect, default_metadata

class Globals(object):

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
	global_connect(app_conf['dburi'])
	default_metadata.create_all()
        # FIXME - EVIL HACK
	# For some unknown reason _engine disappears
	# So we save it here and and restore it each request in __before__
	model.evil_jf = default_metadata.context._engine

    def __del__(self):
        """
        Put any cleanup code to be run when the application finally exits 
        here.
        """
        pass
