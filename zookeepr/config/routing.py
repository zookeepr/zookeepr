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

    # default url scheme
    m.connect(':conroller/new', action='new')
    m.connect(':controller/:id/:action', action='view', id=None)
    
    m.connect('*url', controller='template', action='view')

    return m
