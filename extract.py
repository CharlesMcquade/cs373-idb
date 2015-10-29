# run through the make information and populate the Makes table with its info. 
# Will have to manually edit the table with proper ceo, hq etc...
import json
import io
from app import db
from models import Make, Model, Engine, Type


def pop_makes():
  usmakes = ['ford','dodge','chevrolet','pontiac','chrysler','tesla','jeep','lincoln','gmc','buick','cadillac','hummer','saturn','mercury']
  
  with open('makes.json') as f:
    data = json.load(f)

  for k in data.keys():
    if k in usmakes and Make.query.filter_by(id=data[k]['id']).count() == 0:
      # add all its info to db
      # start by making a Make object 
      m = Make(data[k]['id'],k,data[k]['hq_loc'], data[k]['ceo'],data[k]['est'])
      # add make to session
      db.session.add(m)

  # once all are added, commit session
  db.session.commit()


def pop_models_engines_types():
  # only populate model info where make_id is in the make table
  allm = Make.query.all()
  make_names = list()
  for x in range(len(allm)):
    make_names.append(allm[x].name)

  with open('json/v2_all_with_data/models_refined.json') as f:
    mdata = json.load(f)  # TODO loads() or load()?
  with open ('json/v2_all_with_data/engines.json') as f: 
    edata = json.load(f)
  with open('json/v2_all_with_data/types.json') as f:
    tdata = json.load(f)

  for k in mdata.keys():
    if k in make_names:
      for k2 in mdata[k].keys():
        #make a model object 
        # TODO are we creating a new id here or using the given one? I also still need 
        # to find out if need engine_id here? How are these things being related? 
        # "ford": {"f-450-super-duty": {"transmission_id": "200688291", "engine_id": "200688290", "id": "Ford_F_450_Super_Duty", "make_id": 200005143, "mpg_highway": "Unknown", "mpg_city": "Unknown", "type_id": "4890", "num_doors": "4", "price": 51910.0, "year": 2015}
        try:
          m = Model(mdata[k][k2]['id'], k2, mdata[k][k2]['year'], mdata[k][k2]['price'], mdata[k][k2]['transmission_id'], mdata[k][k2]['make_id'])
        except KeyError:
          continue

        # Now add engine for this vehicle to Engine table since we already have engine_id, 
        # and we know this will be in out 'American' list
        eid = mdata[k][k2]['engine_id']
        e = Engine.query.filter_by(engine_name=edata[eid]['name'], cylinders=edata[eid]['cylinders'], hp=edata[eid]['hp'], torque=edata[eid]['torque'], size=edata[eid]['size'], fuel=edata[eid]['type']).first()
        print('e:', e)
        print()
        if not e:
          e = Engine(eid, edata[eid]['name'], edata[eid]['cylinders'], edata[eid]['hp'], edata[eid]['torque'], edata[eid]['size'], edata[eid]['type'])
        
        m.engines.append(e)

	# Do the same for type since we have the type_id
        tid = mdata[k][k2]['type_id']
        t = Type.query.filter_by(type_name=tdata[tid]['submodel'], doors=mdata[k][k2]['num_doors']).first()
        if not t:
          t = Type(tid, tdata[tid]['submodel'], mdata[k][k2]['num_doors'])
          #db.session.add(t)

        m.types.append(t)
       

        # Add model at end in case we had to append engine or type
        #if Model.query.filter_by(id=mdata[k][k2]['id']).count() == 0:
        db.session.add(m)

  db.session.commit()


if __name__ == "__main__":
  pop_makes()
  pop_models_engines_types()
