"""
Setup your Routes options here
"""
import sys, os

from routes.base import Mapper

def make_map():
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    m = Mapper(directory=root_path+'/controllers')
    
    # Define your routes
    m.connect('home', '', controller='home')
    m.connect(':controller/:action/:id')
    m.connect('*url', controller='template', action='view')

    return m
