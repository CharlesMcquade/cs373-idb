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
    m = Make(2, 'dodge', 'austin', 'Chad Walker', 2000)
    n = Make(3, 'ford', 'dallas', 'Brian Miller', 1999)
    db.session.add(m)
    db.session.add(n)
    r = Make.query.all()
    self.assertEqual({'ford','dodge'}, {x.name for x in r})
    db.session.delete(m)
    db.session.delete(n)

  def test_make_3 (self) :
    # Add to table. Get by PK id. Delete objects. Assert empty
    m = Make(4, 'pontiac', 'dallas', 'Brian Miller', 1999)
    n = Make(5, 'chrysler', 'austin', 'Chad Walker', 2000)
    db.session.add(m)
    db.session.add(n)
    f = Make.query.get(4)
    d = Make.query.get(5)
    db.session.delete(f)
    db.session.delete(d)
    r = Make.query.all()
    self.assertEqual([], r)
    
  def test_make_4 (self) :
    m = Make(5, 'cadillac', 'dallas', 'Brian Miller', 1999)
    self.assertEqual(m.json, {'ceo': 'Brian Miller', 'established': 1999, 'id': 5, 'name': 'cadillac', 'model_ids': [], 'models': [], 'hq': 'dallas'})

  # -------
  # Model
  # -------
  def test_model_1 (self) :
    # def __init__(self, id, name, year, price, trans, make_id):
    m = Model('model_1', 'ram', 2015, 50000, 'manual', 1234)
    db.session.add(m)
    #db.session.commit()
    r = Model.query.filter_by(name='ram').first()
    self.assertEqual('ram', r.name)
    db.session.delete(m)
    #db.session.commit()
 
  def test_model_2 (self) :
    m = Model('model_2', 'neon', 2009, 8000, 'automatic', 1234)
    db.session.add(m)
    #db.session.commit()
    r = Model.query.filter_by(name='neon').first()
    self.assertEqual('neon', r.name)
    db.session.delete(m)
    #db.session.commit()
 
  def test_model_3 (self) :
    # Add to table. Get by PK id. Delete objects. Assert empty
    m = Model('model_3', 'ram', 2015, 55000, 'manual', 1234)
    n = Model('model_4', 'neon', 2009, 8999, 'automatic', 1234)
    db.session.add(m)
    db.session.add(n)
    f = Model.query.get('model_3')
    d = Model.query.get('model_4')
    db.session.delete(f)
    db.session.delete(d)
    r = Model.query.all()
    self.assertEqual([], r)
  
  def test_model_4 (self):
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
    #if not Engine.query.get(1):
    db.session.add(e)
    #db.session.commit()
    r = Engine.query.filter_by(name='4cyl').first()
    self.assertEqual('4cyl', r.name)
    db.session.delete(e)
   # db.session.commit()

  def test_engine_2 (self) :
    e = Engine(2, 'V8', 8, 9000, 505, 5.0, 'diesel')
    db.session.add(e)
    #db.session.commit()
    r = Engine.query.filter_by(id = 2).first()
    self.assertEqual( 9000, r.hp)
    db.session.delete(e)
    #db.session.commit()

  def test_engine_3 (self) :
    a = Engine(3, '4cyl', 4, 30, 50, 2, 'gasoline')
    b = Engine(4, 'V8', 8, 900, 50, 5, 'diesel')
    db.session.add(a)
    db.session.add(b)
    f = Engine.query.get(3)
    d = Engine.query.get(4)
    db.session.delete(f)
    db.session.delete(d)
    r = Model.query.all()
    self.assertEqual([], r)

  def test_engine_4 (self) :
    e = Engine(7, '4cyl', 4, 30, 50, 2, 'gasoline')
    m = Model('model_7', 'ram', 2015, 55000, 'manual', 6)
    m.engines.append(e)
    self.assertEqual(e.json, {'hp': 30, 'models': ['ram'], 'fuel': 'gasoline', 'cylinders': 4, 'model_ids': ['model_7'], 'size': 2, 'name': '4cyl', 'id': 7, 'torque': 50})
 
  # -------
  # Type
  # -------
  def test_type_1 (self) :
    a = Type(1, 'suv', 5)
    db.session.add(a)
    r = Type.query.get(1)
    self.assertEqual(5, r.doors)
    db.session.delete(a)

  def test_type_2 (self) :
    a = Type(2, 'sedan', 4)
    db.session.add(a)
    r = Type.query.get(2)
    self.assertEqual('sedan', r.name)
    db.session.delete(a)

  def test_type_3 (self) :
    a = Type(3, 'truck', 5)
    b = Type(4, 'van', 4)
    db.session.add(a)
    db.session.add(b)
    f = Type.query.get(3)
    d = Type.query.get(4)
    db.session.delete(f)
    db.session.delete(d)
    r = Type.query.all()
    self.assertEqual([], r)

  def test_type_4 (self) :
    m = Model('model_8', 'ram', 2015, 55000, 'manual', 6)
    t = Type(8, 'truck', 5)
    m.types.append(t)
    self.assertEqual(t.json, {'name': 'truck', 'models': ['ram'], 'doors': 5, 'id': None, 'model_ids': ['model_8']})


if __name__ == "__main__" :
  main()
