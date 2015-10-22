#import os 
#import sys
#from sqlalchemy import db.Column, ForeignKey, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
#from slqalchemy.orm import relationship
#from sqlalchemy import create_engine
#
#Base = declarative_base()
#
# might not need all the above. Following tutorial
# assuming db = SQLAlchemy

# TODO: Verify Make, Model, and Engine use external PK

from app import db

class Make(db.Model):
  """
  Table to store Make details.
  id: external PK used in model.make_id as FK
  models: relationship to Model class. Each model instance will
  have a field model.make that points back to the Make class. 
  A model then can find its make with model.make.name although
  no make attribute exists in the model schema.
  make.models will return a query object which can then be used to
  to select from since it is declared as 'dynamic'
  """
  __tablename__ = 'make'
  id = db.Column(Integer, primary_key=True)
  name = db.Column(String(15), nullable=False)
  hqlocation = db.Column(String(250))
  ceo = db.Column(String(250))
  established = db.Column(Integer)
  models = db.relationship('Model', backref='make', lazy='dynamic')

  def __init__(self, id, name, hqlocation, ceo, established):
    self.id = id
    self.name = name
    self.hqlocation = hqlocation
    self.ceo = ceo
    self.established = established

  def __repr__(self):
    return '<Make %r>' % (self.name)

class Model(db.Model):
  """
  Table to store model details.
  id: external PK used in ModelEngine and ModelType junction tables
  to grab all engines and types that are associated with 
  this model. 
  make_id: FK, linked to Make.id
  Can reference Make through relationship backref make. 
  """
  __tablename__ = 'model'
  id = db.Column(String, primary_key=True)
  model_name = db.Columnn(String(25), nullable=False)
  year = db.Column(Integer)
  price = db.Column(Integer)
  transmission = (String(250))
  make_id = db.Column(Integer, ForeignKey('make.id'))
  
  # models <-> engines relationship
  engines = relationship("Engine", secondary=model_engine, backref="models", lazy="dynamic")
  # models <-> types relationship
  types = relationship("Type", secondary=model_type, backref="models", lazy="dynamic")

  def __init__(self, id, name, year, price, trans, make_id):
    self.id = id
    self.model_name = name
    self.year = year
    self.price = price
    self.transmission = trans
    self.make_id = make_id

  def __repr__(self):
    return '<Model %r>' % (self.name)

class Engine(db.Model):
  """
  Table to store engine details, such as number of cylinders,
  horse power, fule type, size in liters, etc. 
  id: external PK, link to ModelEngine.engine_id as FK
  """
  __tablename__ = 'engine'
  id = db.Column(Integer, primary_key=True)
  engine_name = db.Column(string(250))
  cylinders = db.Column(Integer)
  hp = db.Column(Integer)
  torque = db.Column(Integer)
  size = db.Column(Integer)
  fuel = db.Column(String(50))

  def __init__(self, id, name, cyl, hp, tor, size, fuel):
    self.id = id
    self.engine_name = name
    self.cylinders = cyl
    self.hp = hp
    self.torque = tor
    self.size = size
    self.fuel = fuel

  def __repr__(self):
    return '<Engine %r>' % (self.name)


class Type(db.Model):
  """
  Table to store type of vehicle and number of doors
  id: auto increment PK, linked to ModelType.type_id as FK
  type_name: type of vehicle (SUV, Truck Convertible, etc)
  """
  __tablename__ = 'type'
  id = db.Column(Integer, primary_key=True)
  type_name = db.Column(String(25))
  doors = db.Column(Integer)

  def __init__(self, name, doors):
    self.type_name = name
    self.doors = doors

  def __repr__(self):
    return '<Type %r>' % (self.name)


# association tables for model<>engine, and model<>type
model_engine = Table('model_engine', db.metadata, Colummn('model_id', Integer, ForeignKey('model.id')), Column('engine_id', Integer, ForeignKey('engine.id')))

model_type = Table('model_type', db.metadata, Column('model_id', Integer, ForeignKey('model.id')), Column('type_id', Integer, ForeignKey('type.id')))

# |
# V These may not be if the metadata association tables above work

class ModelEngine(db.Model):
  """
  Junction table used to map the many to many relationship 
  of models and engines. 
  model_id: FK, link to model.id 
  engine_id: FK, link to engine.id 
  Example query: 
  SELECT model_name, engine_name FROM ModelEngine 
  JOIN Model ON Model.id = ModelEngine.model_id JOIN Engine
  ON Engine.id = ModelEngine.engine_id
  """
  __tablename__ = 'modelengine'
  model_id = db.Column(String, ForeignKey('model.id'))
  engine_id = db.Column(Integer, ForeignKey('engine.id'))
  PrimaryKeyConstraint('model_id', 'engine_id', name='modelengine_id')

  def __init__(self, mid, eid):
    self.model_id = mid
    self.engine_id = eid
 

class ModelType(db.Model):
  """
  Junction table used to map the many to many relationship
  of models and types. 
  model_id: FK, link to model.id 
  type_id: FK, link to type.id 
  Example query:
  SELECT model_name, type_name, FROM ModelEngine
  JOIN Model ON Model.id = ModelType.model_id JOIN Type 
  ON Type.id = ModelType.type_id
  """
  __tablename__ = "modeltype"
  model_id = db.Column(Integer, ForeignKey('model.id'))
  type_id = db.Column(Integer, ForeignKey('type.id'))
  PrimaryKeyConstraint('model_id', 'engine_id', name='modeltype_id')

  def __init__(self, mid, tid):
    self.model_id = mid
    self.type_id = tid
