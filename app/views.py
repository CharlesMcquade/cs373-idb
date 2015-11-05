from flask import render_template, redirect, abort, request, jsonify
from jinja2 import TemplateNotFound
from app import app
import json
import subprocess
from app import db
from models import Make, Model, Engine, Type, Transmission

#with open('dat/engines.json') as i : engine_dict = json.load(i)
#with open('dat/makes.json') as i : makes_dict = json.load(i)
#with open('dat/models.json') as i : models_dict = json.load(i)
#with open('dat/types.json') as i : types_dict = json.load(i)
#with open('dat/transmissions.json') as i : tranny_dict = json.load(i)

query_dict = {'engines' : (Engine, 
							["Name", "Size (Liters)", "Cylinders", "Horsepower", "Fuel Type", "Torque", "Models"],
			  				["name", "size", "cylinders", "hp", "fuel", "torque", "models"]),
			  'models' : (Model, 
			  				["Name", "Make", "Year", "Price", "Engine ID", "Type", "Transmission ID"],
			  				["name", "make", "year", "price", "engines", "types", "transmissions"]),
			  'types' : (Type, 
			  				["Name", "Number of Doors", "Models"],
			  				["name", "doors", "models"]),
			  'transmissions' : (Transmission, 
			  				["Name", "Transmission Type", "Automatic Type", "Number of Speeds", "Models"],
			  				["name", "transmission_type", "automatic_type", "num_speeds", "models"]),
			  'makes' : (Make, 
			  				["Name", "Headquarters Location", "CEO", "Date Established", "Models"],
			  				["name", "hq", "ceo", "established", "models"])}

# -------
#  index
# -------
@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html')


# ------------
#  all tables
# ------------
@app.route('/<path:path_val>', methods=['GET'])
@app.route('/<path:path_val>/', methods=['GET'])
def tables(path_val):
	try: 
		db, headers, keys = query_dict[path_val]

		queries = dict()
		for arg in request.args:
			queries[arg] = request.args.get(arg)

		t = db.query.filter_by(**queries)

		return render_template('table.html', keys=keys, path=path_val, headers=headers, t=t)
	except TemplateNotFound:
		abort(404)
	except KeyError:
		abort(404)

# ---------
#  engines
# ---------


@app.route('/<path:path_val>/<obj_id>')
def single_engine(path_val, obj_id):
	try :
		db, headers, keys = query_dict[path_val]

		obj = db.query.filter_by(id = obj_id).first()
		if obj == None: raise KeyError

		return render_template('single_engine.html', hk= zip(headers, keys), path=path_val, obj=obj)
	except TemplateNotFound:
		abort(404)
	except KeyError:
		abort(404)



# -------
#  about
# -------
@app.route('/about')
def about():
	return render_template('about.html')


# -------
#  tests
# -------
@app.route('/tests')
def tests():
	cmd = ["make","test"]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	out, err = p.communicate()
	with open('tests.tmp') as f:
		result = f.readlines()
	try :
		return render_template('tests.html', results=result)
	except TemplateNotFound:
		about(404)

# -----------
#  API Calls
# -----------
@app.route('/make_api', methods=['GET'])
def make_api():
	query_dict = dict()
	for arg in request.args:
		query_dict[arg] = request.args.get(arg)
	search = Make.query.filter_by(**query_dict)
	result = dict()
	for m in search:
		result[str(m.id)] = m.json
	return jsonify(**result)
	# if len(request.args) == 0:
	# 	return jsonify(**makes_dict)
	# result = {}
	# for make in makes_dict:
	# 	flag = True
	# 	for param in request.args:
	# 		if str(makes_dict[make][param]) != request.args.get(param):
	# 			flag = False
	# 			break
	# 	if flag:
	# 		result.update({make: makes_dict[make]})
	# return jsonify(**result)


@app.route('/model_api', methods=['GET'])
def model_api():
	query_dict = dict()
	for arg in request.args:
		query_dict[arg] = request.args.get(arg)
	search = Model.query.filter_by(**query_dict)
	result = dict()
	for m in search:
		result[m.id] = m.json
	return jsonify(**result)
	# if len(request.args) == 0:
	# 	return jsonify(**models_dict)
	# result = {}
	# for model in models_dict:
	# 	flag = True
	# 	for param in request.args:
	# 		if str(models_dict[model][param]) != request.args.get(param):
	# 			flag = False
	# 			break
	# 	if flag:
	# 		result.update({model: models_dict[model]})
	# return jsonify(**result)


@app.route('/engine_api', methods=['GET'])
def engine_api():
	query_dict = dict()
	for arg in request.args:
		query_dict[arg] = request.args.get(arg)
	search = Engine.query.filter_by(**query_dict)
	result = dict()
	for m in search:
		result[str(m.id)] = m.json
	return jsonify(**result)
	# if len(request.args) == 0:
	# 	return jsonify(**engine_dict)
	# result = {}
	# for engine in engine_dict:
	# 	flag = True
	# 	for param in request.args:
	# 		if str(engine_dict[engine][param]) != request.args.get(param):
	# 			flag = False
	# 			break
	# 	if flag:
	# 		result.update({engine: engine_dict[engine]})
	# return jsonify(**result)
			


@app.route('/type_api', methods=['GET'])
def type_api():
	query_dict = dict()
	for arg in request.args:
		query_dict[arg] = request.args.get(arg)
	search = Type.query.filter_by(**query_dict)
	result = dict()
	for m in search:
		result[str(m.id)] = m.json
	return jsonify(**result)
	# if len(request.args) == 0:
	# 	return jsonify(**types_dict)
	# result = {}
	# for t in types_dict:
	# 	flag = True
	# 	for param in request.args:
	# 		if str(types_dict[t][param]) != request.args.get(param):
	# 			flag = False
	# 			break
	# 	if flag:
	# 		result.update({t: types_dict[t]})
	# return jsonify(**result)
