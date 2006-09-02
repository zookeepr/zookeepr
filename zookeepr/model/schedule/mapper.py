from sqlalchemy import mapper

from tables import stream
from domain import Stream

# map the Stream domain object onto the stream table
mapper(Stream, stream)
