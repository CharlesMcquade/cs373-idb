from app import db
from models import Make, Model, Engine, Type

def get_makes():
  d = dict()
  for m in Make.query.all():
    d[m] = m.json

  return d
