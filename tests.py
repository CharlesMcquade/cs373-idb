#!/user/bin/python3

# -------
# imports
# -------

import sys
from app import db
from unittest import main, TestCase
from models import Make, Model, Engine, Type


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
    m = Make(2, 'fake_dodge', 'austin', 'Chad Walker', 2000)
    n = Make(3, 'fake_ford', 'austin', 'Brian Miller', 1999)
    db.session.add(m)
    db.session.add(n)
    r = Make.query.filter_by(hqlocation='austin')
    self.assertEqual({'fake_ford','fake_dodge'}, {x.name for x in r})
    db.session.delete(m)
    db.session.delete(n)

  def test_make_3 (self) :
    m = Make(5, 'cadillac', 'dallas', 'Brian Miller', 1999)
    self.assertEqual(m.json, {'name': 'cadillac', 'models': {}, 'ceo': 'Brian Miller', 'id': 5, 'established': 1999, 'hq': 'dallas'})

  # -------
  # Model
  # -------
  def test_model_1 (self) :
    m = Model('model_1', 'ram', 2015, 50000, 'manual', 1234)
    db.session.add(m)
    r = Model.query.filter_by(name='ram').first()
    self.assertEqual('ram', r.name)
    db.session.delete(m)
 
  def test_model_2 (self) :
    m = Model('model_2', 'neon', 2009, 8000, 'automatic', 1234)
    db.session.add(m)
    r = Model.query.filter_by(name='neon').first()
    self.assertEqual('neon', r.name)
    db.session.delete(m)

  def test_model_3 (self):
    e = Engine(99, 'V8', 8, 900, 50, 5, 'diesel')
    m = Make(6, 'cadillac', 'dallas', 'Brian Miller', 1999)
    mod = Model('model_5', 'ram', 2015, 55000, 'manual', 6)
    mod.engines.append(e)
    db.session.add(m)
    db.session.add(mod)
    self.assertEqual(mod.json, {'year': 2015, 'make': 'cadillac', 'transmission': 'manual', 'price': 55000, 'id': 'model_5', 'engines': {99: 'V8'}, 'name': 'ram', 'types': {}})
    db.session.delete(m)
    db.session.delete(mod)
    
  # -------
  # Engine
  # -------
  def test_engine_1 (self) :
    e = Engine(1, '4cyl', 4, 300, 50, 2.5, 'gasoline')
    db.session.add(e)
    r = Engine.query.filter_by(name='4cyl').first()
    self.assertEqual('4cyl', r.name)
    db.session.delete(e)

  def test_engine_2 (self) :
    e = Engine(2, 'V8', 8, 9000, 505, 5.0, 'diesel')
    db.session.add(e)
    r = Engine.query.filter_by(id = 2).first()
    self.assertEqual( 9000, r.hp)
    db.session.delete(e)

  def test_engine_3 (self) :
    e = Engine(7, '4cyl', 4, 30, 50, 2, 'gasoline')
    m = Model('model_7', 'ram', 2015, 55000, 'manual', 6)
    m.engines.append(e)
    self.assertEqual(e.json, {'name': '4cyl', 'models': {'model_7': 'ram'}, 'torque': 50, 'fuel': 'gasoline', 'id': 7, 'cylinders': 4, 'size': 2, 'hp': 30})
 
  # -------
  # Type
  # -------
  def test_type_1 (self) :
    a = Type(11111, 'fake_suv', 55)
    db.session.add(a)
    r = Type.query.filter_by(name='fake_suv').first()
    self.assertEqual(55, r.doors)
    db.session.delete(a)

  def test_type_2 (self) :
    a = Type(22222, 'fake_sedan', 44)
    db.session.add(a)
    r = Type.query.get(22222)
    self.assertEqual('fake_sedan', r.name)
    db.session.delete(a)

  def test_type_3 (self) :
    m = Model('model_8', 'ram', 2015, 55000, 'manual', 6)
    t = Type(88888, 'truck', 55)
    m.types.append(t)
    self.assertEqual(t.json, {'id': 88888, 'name': 'truck', 'models': {'model_8': 'ram'}, 'doors': 55})


if __name__ == "__main__" :
  main()
