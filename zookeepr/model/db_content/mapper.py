from sqlalchemy.orm import mapper, relation
from sqlalchemy.sql import join

from tables import db_content
from domain import DBContent

mapper(DBContent, db_content)
