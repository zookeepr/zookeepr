"""
Setup your Routes options here
"""
import sys, os

from routes.base import Mapper

def make_map():
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    m = Mapper(directory=root_path+'/controllers')
    
    # Define your routes

    # the top level controller is named home
    m.connect('home', '', controller='home')

    # hack the old error handler back in, using the style of the old
    # routes controller.  this is necessary to get the error handler
    # to not 404 when calling itself
    m.connect('/error/:action/:id', controller='error')

    # special case for security controller, again in the style of the
    # original routes controller
    m.connect('/security/:action', controller='security')

    # Note to wary travellers; an ID can never be 'new' because of this
    # routing rule
    m.connect(':controller/new', action='new', id=None)
    m.connect(':controller', action='index', id=None)
    # default action when not specified is 'view'
    m.connect(':controller/:id', action='view')
    # default url scheme
    m.connect(':controller/:id/:action', action='index', id=None)

    m.connect('*url', controller='template', action='view')

    return m
