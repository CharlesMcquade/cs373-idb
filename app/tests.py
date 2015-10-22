#!/user/bin/python3

# -------
# imports
# -------

import sys
from app import db
from unittest import main, TestCase
from models import Make, Model, Engine, Type, ModelEngine, ModelType


class TestModels (TestCase):
  # -------
  # Make
  # -------
  def test_make_1 (self) :
    # Test adding to table and selecting by name
    m = Make(1, 'ford', 'dallas', 'Brian Miller', 1999)
    db.session.add(m)
    r = Make.query.filter_by(name='ford').first()
    self.assertEqual('ford', r.name)
    db.session.delete(m)
    
  def test_make_2 (self) :
    # test adding one more to table and selecting both
    m = Make(2, 'dodge', 'austin', 'Chad Walker', 2000)
    db.session.add(m)
    r = Make.query.all()
    self.assertEqual({'ford','dodge'}, {x.name for x in r})
    db.session.delete(m)

  def test_make_3 (self) :
    # Add to table. Get by PK id. Delete objects. Assert empty
    m = Make(1, 'ford', 'dallas', 'Brian Miller', 1999)
    n = Make(2, 'dodge', 'austin', 'Chad Walker', 2000)
    db.session.add(m)
    db.session.add(n)
    f = Make.query.get(1)
    d = Make.query.get(2)
    db.session.delete(f)
    db.session.delete(d)
    r = Make.query.all()
    self.assertEqual([], r)
    
  # -------
  # Model
  # -------
  def test_model_1 (self) :
    # def __init__(self, id, name, year, price, trans, make_id):
    m = Model(1, 'ram', 2015, 50000, 'manual', 1234)
    db.session.add(m)
    db.session.commit()
    r = Model.query.filter_by(model_name='ram').first()
    self.assertEqual('ram', r.model_name)
    db.session.delete(m)
    db.session.commit()
 
  def test_model_2 (self) :
    m = Model(2, 'neon', 2009, 8000, 'automatic', 1234)
    db.session.add(m)
    db.session.commit()
    r = Model.query.filter_by(model_name='neon').first()
    self.assertEqual('neon', r.model_name)
    db.session.delete(m)
    db.session.commit()
 
  def test_model_3 (self) :
    # Add to table. Get by PK id. Delete objects. Assert empty
    m = Model(1, 'ram', 2015, 50000, 'manual', 1234)
    n = Model(2, 'neon', 2009, 8000, 'automatic', 1234)
    db.session.add(m)
    db.session.add(n)
    f = Model.query.get(1)
    d = Model.query.get(2)
    db.session.delete(f)
    db.session.delete(d)
    r = Model.query.all()
    self.assertEqual([], r)
 
  # -------
  # Engine
  # -------
  def test_engine_1 (self) :
    e = Engine(1, '4cyl', 300, 50, 2.5, 'gasoline')
    db.session.add(e)
    db.session.commit()
    r = Engine.query.filter_by(engine_name='4cl').first()
    self.assertEqual('4cl', r.engine_name)
    db.session.delete(e)
    db.session.commit()

  def test_engine_2 (self) :
    e = Engine(2, 'V8', 9000, 505, 5.0, 'diesel')
    db.session.add(e)
    db.session.commit()
    r = Engine.query.filter_by(id = 2).first()
    self.assertEqual('9000', r.hp)
    db.session.delete(e)
    db.session.commit()

  def test_engine_3 (self) :
    a = Engine(1, '4cyl', 300, 50, 2.5, 'gasoline')
    b = Engine(2, 'V8', 9000, 505, 5.0, 'diesel')
    db.session.add(a)
    db.session.add(b)
    f = Engine.query.get(1)
    d = Engine.query.get(2)
    db.session.delete(f)
    db.session.delete(d)
    r = Model.query.all()
    self.assertEqual([], r)
 
  # -------
  # Type
  # -------
  def test_type_1 (self) :
    a = Type('suv', 5)
    db.session.add(a)
    r = Type.query.get(1)
    self.assertequal('5', r.doors)
    db.sessin.delete(a)

  def test_type_2 (self) :
    a = Type('sedan', 4)
    db.session.add(a)
    r = Type.query.get(1)
    self.assertequal('sedan', r.type_name)
    db.sessin.delete(a)

  def test_type_3 (self) :
    a = Type('suv', 5)
    b = Type('sedan', 4)
    db.session.add(a)
    db.session.add(b)
    f = Engine.query.get(1)
    d = Engine.query.get(2)
    db.session.delete(f)
    db.session.delete(d)
    r = Engine.query.all()
    self.assertEqual([], r)
 
