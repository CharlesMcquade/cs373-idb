from app import db
"""
Models.py defines the database models using Python classes. These classes will be transformed into MySQL tables, the variables in the class making the attributes of the table, by the Flask SQLAlchemy module.
"""

# association tables for model<>engine, and model<>type
model_engine = db.Table('model_engine', db.Column('model_id', db.String(50), db.ForeignKey('model.id')),db.Column('engine_id', db.Integer, db.ForeignKey('engine.id')))
model_type = db.Table('model_type', db.Column('model_id', db.String(50), db.ForeignKey('model.id')), db.Column('type_id', db.Integer, db.ForeignKey('type.id')))
model_transmission = db.Table('model_transmission', db.Column('model_id', db.String(50), db.ForeignKey('model.id')),db.Column('transmission_id', db.Integer, db.ForeignKey('transmission.id')))


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
    return '%r' % (self.name)
  
  @property
  def json(self):
    model_dict = dict()
    for mobj in self.models.all():
      model_dict[mobj.id] = mobj.name
    return {'id':self.id, 'name':self.name, 'hq':self.hqlocation, 'ceo': self.ceo, 'established':self.established, 'models': model_dict}

class Model(db.Model):
  """
  Table to store vehicle model details.
  Each model can reference its make using model.make since a relationship backreference is established in the Make class.
  The association tables model_engine and model_class declared as metadata to the database are used to link the many to many relationships to models and engines, and models and types. 
  id: an external Primary Key. Used in model_engine and  model_type association tables.
  make_id: a Foreign Key linked to Make.id.
  """
  __tablename__ = 'model'
  id = db.Column(db.String(50), primary_key=True)
  name = db.Column(db.String(25), nullable=False)
  year = db.Column(db.Integer)
  price = db.Column(db.Integer)
  transmission = db.Column(db.String(250))
  make_id = db.Column(db.Integer, db.ForeignKey('make.id'))
  
  engines = db.relationship("Engine", secondary=model_engine, backref=db.backref("models", lazy="dynamic"), lazy="dynamic")

  types = db.relationship("Type", secondary=model_type, backref=db.backref("models", lazy="dynamic"), lazy="dynamic")

  transmissions = db.relationship("Transmission", secondary=model_transmission, backref=db.backref("models", lazy="dynamic"), lazy="dynamic")

  def __init__(self, id, name, year, price, trans, make_id):
    self.id = id
    self.name = name
    self.year = year
    self.price = price
    self.transmission = trans
    self.make_id = make_id

  def __repr__(self):
    return '%r' % (self.name)

  @property
  def json(self):
    engine_dict = dict()
    type_dict = dict()
    for eobj in self.engines.all():
      engine_dict[eobj.id] = eobj.name
    for tobj in self.types.all():
      type_dict[tobj.id] = tobj.name
    return {'id':self.id, 'name':self.name, 'year':self.year, 'price':self.price, 'transmission': self.transmission, 'make':self.make.name, 'engines':engine_dict, 'types':type_dict}

class Engine(db.Model):
  """
  Table to store engine details. 
  The Engine model is a many to many relationship with the Model class. A vehicle model can have numberous engines and a single engine can belong to multiple vehicles. 
   An Engine object has a models attribute that is not explicitly declared, but is established through the relationship that exists within the Model class. 
  An Engine object can retrieve a query object of the models it pertains to by using engine.models.
  """
  __tablename__ = 'engine'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(250))
  cylinders = db.Column(db.Integer)
  hp = db.Column(db.Integer)
  torque = db.Column(db.Integer)
  size = db.Column(db.Integer)
  fuel = db.Column(db.String(50))
  __table_args__ = (db.UniqueConstraint('name', 'cylinders', 'hp', 'torque', 'size', 'fuel', name='engine_uc'),)

  def __init__(self, id, name, cyl, hp, tor, size, fuel):
    self.id = id
    self.name = name
    self.cylinders = cyl
    self.hp = hp
    self.torque = tor
    self.size = size
    self.fuel = fuel

  def __repr__(self):
    return '%r' % (self.name)

  @property
  def json(self):
    model_dict = dict()
    for mobj in self.models.all():
      model_dict[mobj.id] = mobj.name
    return {'id':self.id, 'name':self.name, 'cylinders':self.cylinders, 'hp':self.hp, 'torque':self.torque, 'size':self.size, 'fuel':self.fuel, 'models':model_dict}


class Type(db.Model):
  """
  Table to store type of vehicle. 
  Vehicle type referes to the class or style of vehicle. For example: SUV, Truck, Coupe, etc.
  id: an auto incrementing Primary Key, linked to ModelType.type_id as a Foreign Key.
  name: type of vehicle (SUV, Truck Convertible, etc)
  The Type class shares a many to many relationship to the Model class and is able to reference a query object of its models using type.model.
  """
  __tablename__ = 'type'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(25))
  doors = db.Column(db.Integer)
  __table_args__ = (db.UniqueConstraint('name', 'doors', name='type_uc'),)

  def __init__(self, tid, name, doors):
    self.id = tid
    self.name = name
    self.doors = doors

  def __repr__(self):
    return '%r' % (self.name)

  @property 
  def json(self):
    model_dict = dict()
    for mobj in self.models.all():
      model_dict[mobj.id] = mobj.name
    return {'id':self.id, 'name':self.name, 'doors':self.doors, 'models':model_dict}

class Transmission(db.Model):
  """
  Table to store transmission details.
  The Transmission model is designed very similarly to the Engine and Type classes. It shares a many to many relationship with the Model class. A vehicle model might have multiple transmissions, such as a manual and automatic version, and many vehicles share common transmissions. 
  The Transmission class does not have a declared models attribute, but the models it it pertains to can be accessed via the 'tranmissions' relationship in the Models class. 
  The query tranmission_object.models would return a list of models. 
  """
  __tablename__ = 'transmission'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(250))
  transmission_type = db.Column(db.String(50))
  automatic_type = db.Column(db.String(50))
  num_speeds = db.Column(db.Integer)
  __table_args__ = (db.UniqueConstraint('name', 'transmission_type', 'automatic_type', 'num_speeds', name='transmission_uc'),)

  def __init__(self, id, name, transmission_type, automatic_type, num_speeds):
    self.id = id
    self.name = name
    self.transmission_type = transmission_type
    self.automatic_type = automatic_type
    self.num_speeds = num_speeds

  def __repr__(self):
    return '%r' % (self.name)

  @property
  def json(self):
    model_dict = dict()
    for mobj in self.models.all():
      model_dict[mobj.id] = mobj.name
    return {'id':self.id, 'name':self.name, 'transmission_type':self.transmission_type, 'automatic_type':self.automatic_type, 'num_speeds':self.num_speeds, 'models':model_dict}


