from sqlalchemy import mapper, join, relation

from tables import openday
from domain import Openday

mapper(Openday, openday)
