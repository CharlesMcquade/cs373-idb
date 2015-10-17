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

from app import db

class Make(Base):
  __tablename__ = 'make'
  id = db.Column(Integer, primary_key=True)
  name = db.Column(String(15), nullable=False)
  hqlocation = db.Column(String(250))
  ceo = db.Column(String(250))
  established = db.Column(Integer)

  def __repr__(self):
    return '<Make %r>' % (self.name)

class Model(Base):
  __tablename__ = 'model'
  id = db.Column(Integer, primary_key=True)
  name = db.Columnn(String(25), nullable=False)
  year = db.Column(Integer)
  price = db.Column(Integer)
  transmission = (String(250))
  engine_id = db.Column(Integer, ForeignKey('engine.key')) 
  type_id = db.Column(Integer, ForeignKey('type.id'))
  make_id = db.Column(Inteer, ForeignKey('make.id'))
# if we need to link this to its make, do we do a backref

  def __repr__(self):
    return '<Model %r>' % (self.name)

class Engine(Base):
  __tablename__ = 'engine'
  id = db.Column(Integer, primary_key=True)
  name = db.Column(string(250))
  cylinders = db.Column(Integer)
  hp = db.Column(Integer)
  torque = db.Column(Integer)
  size = db.Column(Integer)
  fuel = db.Column(String(50))

  def __repr__(self):
    return '<Engine %r>' % (self.name)

class Type(Base):
  __tablename__ = 'type'
  id = db.Column(Integer, primary_key=True)
  name = db.Column(String(25))
  doors = db.Column(Integer)

  def __repr__(self):
    return '<Type %r>' % (self.name)

# Create engine that stores data in murikinmade.db
#engine = create_engine('mysql:///murikinmade.db')

# Create all tables in the engine
#Base.metadata.create_all(engine)
