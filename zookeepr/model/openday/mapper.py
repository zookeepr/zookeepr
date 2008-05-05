from sqlalchemy.orm import mapper, relation
from sqlalchemy.sql import join

from tables import openday
from domain import Openday

mapper(Openday, openday)
