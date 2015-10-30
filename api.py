from app import db
from models import Make, Model, Engine, Type

def get_makes(id=None):
  d = dict()
  if id is None:
    for m in Make.query.all():
      d[m.name] = m.json
    return d

  return Make.query.filter_by(id=id).first().json

def get_models(id=None):
  d = dict()
  if id is None:
    for m in Model.query.all():
      d[m.name] = m.json
    return d

  return Model.query.filter_by(id=id).first().json

def get_engines(id=None):
  d = dict()
  if id is None:
    for e in Engine.query.all():
      d[e.name] = e.json
    return d

  return Engine.query.filter_by(id=id).first().json

def get_types(id=None):
  d = dict()
  if id is None:
    for t in Type.query.all():
      d[t.name] = t.json
    return d

  return Type.query.filter_by(id=id).first().json




