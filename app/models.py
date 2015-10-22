from app import db
"""
Models.py defines the database models using Python classes. These classes will be transformed into MySQL tables, the variables in the class making the attributes of the table, by the Flask SQLAlchemy module.
"""

# association tables for model<>engine, and model<>type
model_engine = db.Table('model_engine', db.metadata, db.Column('model_id', db.Integer, db.ForeignKey('model.id')), db.Column('engine_id', db.Integer, db.ForeignKey('engine.id')))
model_type = db.Table('model_type', db.metadata, db.Column('model_id', db.Integer, db.ForeignKey('model.id')), db.Column('type_id', db.Integer, db.ForeignKey('type.id')))


class Make(db.Model):
  """
  Table to store vehicle make (manufacturer) details.
  id: an external Primary Key. Used in model.make_id as a Foreign Key.
  models: a relationship to the Model class. This allows each model instance to have a field model.make that points back to the Make class. 
  A model then can find its make with model.make.name although no make attribute exists in the model schema. 
  The lazy parameter of the relationship causes make.models to return a query object which can then be used to select from.
  """
  __tablename__ = 'make'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(15), nullable=False)
  hqlocation = db.Column(db.String(250))
  ceo = db.Column(db.String(250))
  established = db.Column(db.Integer)
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
  Table to store vehicle model details.
  Each model can reference its make using model.make since a relationship backreference is established in the Make class.
  The association tables model_engine and model_class declared as metadata to the database are used to link the many to many relationships to models and engines, and models and types. 
  id: an external Primary Key. Used in model_engine and  model_type association tables.
  make_id: a Foreign Key linked to Make.id.
  """
  __tablename__ = 'model'
  id = db.Column(db.String, primary_key=True)
  model_name = db.Column(db.String(25), nullable=False)
  year = db.Column(db.Integer)
  price = db.Column(db.Integer)
  transmission = db.Column(db.String(250))
  make_id = db.Column(db.Integer, db.ForeignKey('make.id'))
  
  # models <-> engines relationship
  engines = db.relationship("Engine", secondary=model_engine, backref="models", lazy="dynamic")
  # models <-> types relationship
  types = db.relationship("Type", secondary=model_type, backref="models", lazy="dynamic")

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
  Table to store engine details. 
  The Engine model is a many to many relationship with the Model class. A vehicle model can have numberous engines and a single engine can belong to multiple vehicles. 
  An Engine object has a models attribute that is not explicitly declared, but is established through the relationship that exists within the Model class. 
  An Engine object can retrieve a query object of the models it pertains to by using engine.models.
  """
  __tablename__ = 'engine'
  id = db.Column(db.Integer, primary_key=True)
  engine_name = db.Column(db.String(250))
  cylinders = db.Column(db.Integer)
  hp = db.Column(db.Integer)
  torque = db.Column(db.Integer)
  size = db.Column(db.Integer)
  fuel = db.Column(db.String(50))

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
  Table to store type of vehicle. 
  Vehicle type referes to the class or style of vehicle. For example: SUV, Truck, Coupe, etc.
  id: an auto incrementing Primary Key, linked to ModelType.type_id as a Foreign Key.
  type_name: type of vehicle (SUV, Truck Convertible, etc)
  The Type class shares a many to many relationship to the Model class and is able to reference a query object of its models using type.model.
  """
  __tablename__ = 'type'
  id = db.Column(db.Integer, primary_key=True)
  type_name = db.Column(db.String(25))
  doors = db.Column(db.Integer)

  def __init__(self, name, doors):
    self.type_name = name
    self.doors = doors

  def __repr__(self):
    return '<Type %r>' % (self.name)


# |
# V These may not be if the metadata association tables above work
'''
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
  model_id = db.Column(db.String, db.ForeignKey('model.id'))
  engine_id = db.Column(db.Integer, db.ForeignKey('engine.id'))
  db.PrimaryKeyConstraint('model_id', 'engine_id', name='modelengine_id')

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
  model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
  type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
  db.PrimaryKeyConstraint('model_id', 'engine_id', name='modeltype_id')

  def __init__(self, mid, tid):
    self.model_id = mid
    self.type_id = tid
'''
