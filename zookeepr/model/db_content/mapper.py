from sqlalchemy.orm import mapper, relation
from sqlalchemy.sql import join

from tables import db_content_type, db_content
from domain import DBContentType, DBContent

mapper(DBContentType, db_content_type)
mapper(DBContent, db_content, properties = {'type': relation(DBContentType)})
