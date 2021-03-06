from flask import render_template, redirect, abort, request, jsonify
from jinja2 import TemplateNotFound
from app import app
import json
import subprocess
from app import db
from models import Make, Model, Engine, Type, Transmission
import search
import refine_search

with open('app/static/json/coords.json') as i:
	tweet_coords = json.load(i)


def make_anchor(a, t) : return '<a href="{}">{}</a>'.format(a, t)
def make_engine_name(d) : return '{}L V{} {}'.format(d.size, d.cylinders, d.fuel)
def search_make_engine_name(q) : return '{}L V{} {}'.format(d['size'], d['cylinders'], d['fuel'])
def make_tran_name(d) :
	if d.num_speeds == "continuously variable" :
		return "Variable Transmission"
	return "{}-Speed {}".format(d.num_speeds, d.transmission_type.lower())
def make_tran_auto_type(s) :
	if str(s).lower() == 'false' : return "Not applicable"
	else : return make_anchor("/transmissions?automatic_type={}".format(s), s)

#dictionary for queries.
# key = path,
# value= tuple(Database, Proper Titles for Data values, Data index values, functions to apply to titles/values)
query_dict = {'engines' : (Engine,
							["Name", "Size (Liters)", "Cylinders", "Horsepower", "Fuel Type", "Torque", "Models"],
			  				["name", "size", "cylinders", "hp", "fuel", "torque", "models"],
			  				[(lambda h, d:
			  					(h, make_anchor("/engines/{}".format(d.id), make_engine_name(d)))),
			  				 (lambda h, d:
			  					(h, make_anchor("/engines?size={}".format(d.size), d.size))),
		  					 (lambda h, d:
			  					(h, make_anchor("/engines?cylinders={}".format(d.cylinders), d.cylinders))),
		  					 (lambda h, d:
			  					(h, make_anchor("/engines?hp={}".format(d.hp), d.hp))),
			  				 (lambda h, d:
			  					(h, make_anchor("/engines?fuel={}".format(d.fuel), d.fuel))),
			  				 (lambda h, d:
			  					(h, make_anchor("/engines?torque={}".format(d.torque), d.torque))),
			  				 (lambda h, d:
			  					(h, make_anchor("/models/engines?id={}".format(d.id), "All Models with this Engine")))]),
			  'models' : (Model,
			  				["Name", "Make", "Year", "Price", "Engine", "Type", "Transmission"],
			  				["name", "make", "year", "price", "engines", "types", "transmissions"],
			  				[(lambda h, d:
			  					(h, make_anchor("/models/{}".format(d.id), d.name.title()))),
			  				(lambda h, d:
			  					(h, make_anchor("/makes/{}".format(d.make.id), d.make.name.title()))),
			  				(lambda h, d:
			  					(h, make_anchor("/models/?year={}".format(d.year), d.year))),
			  				(lambda h, d:
			  					(h, "${:.2f}".format(float(d.price)))),
			  				(lambda h, d:
			  					(h, make_anchor("/engines/{}".format(d.engines.first().id), make_engine_name(d.engines.first())))),
			  				(lambda h, d:
			  					(h, make_anchor("/types/{}".format(d.types.first().id), d.types.first().name))),
			  				(lambda h, d:
			  					(h, make_anchor("/transmissions/{}".format(d.transmissions.first().id), make_tran_name(d.transmissions.first()))))]),
			  'types' : (Type,
			  				["Name", "Number of Doors", "Models"],
			  				["name", "doors", "models"],
			  				[(lambda h, d: (h, make_anchor("/types/{}".format(d.id), d.name.title()))),
			  				 (lambda h, d: (h, make_anchor("/types?doors={}".format(d.doors), d.doors))),
			  				 (lambda h, d: (h, make_anchor("/models/types?id={}".format(d.id), "All Models of this Type")))]),
			  'transmissions' : (Transmission,
			  				["Name", "Transmission Type", "Automatic Type", "Number of Speeds", "Models"],
			  				["name", "transmission_type", "automatic_type", "num_speeds", "models"],
			  				[(lambda h, d: (h, make_anchor("/transmissions/{}".format(d.id), make_tran_name(d)))),
			  				 (lambda h, d: (h, make_anchor("/transmissions?transmission_type={}".format(d.transmission_type), d.transmission_type))),
			  				 (lambda h, d: (h, make_tran_auto_type(d.automatic_type))),
			  				 (lambda h, d: (h, make_anchor("/transmissions?num_speeds={}".format(d.num_speeds), d.num_speeds))),
			  				 (lambda h, d: (h, make_anchor("/models/transmissions?id={}".format(d.id), "All Models with this Transmission")))]),
			  'makes' : (Make,
			  				["Name", "Headquarters Location", "CEO", "Date Established", "Models"],
			  				["name", "hqlocation", "ceo", "established", "models"],
			  				[(lambda h, d: (h, make_anchor("/makes/{}".format(d.id), d.name.title()))),
			  				 (lambda h, d: (h, d.hqlocation)),
			  				 (lambda h, d: (h, d.ceo)),
			  				 (lambda h, d: (h, d.established)),
			  				 (lambda h, d: (h, make_anchor("/models/makes?id={}".format(d.id), "All Models of this Make")))])}


# -------
#  index
# -------
@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html')


# ---------------------
#  view for all tables
# ---------------------
@app.route('/<path:path_val>', methods=['GET'])
@app.route('/<path:path_val>/', methods=['GET'])
def tables(path_val):
	try:
		db, headers, keys, functions = query_dict[path_val]

		queries = dict()
		for arg in request.args:
			queries[arg] = request.args.get(arg)

		t = db.query.filter_by(**queries)

		return render_template('table.html',
									z=zip,
									keys=keys,
									functions=functions,
									path=path_val,
									headers=headers,
									t=t)
	except TemplateNotFound:
		abort(404)
	except KeyError:
		abort(404)

# -------------------
#  view for all items
# -------------------
@app.route('/<path:path_val>/<obj_id>', methods=['GET'])
def single_item(path_val, obj_id):
	try :
		queries = dict()
		for arg in request.args:
			queries[arg] = request.args.get(arg)

		if len(queries) < 1 :
			db, headers, keys, functions = query_dict[path_val]
			obj = db.query.filter_by(id = obj_id).first()
			if obj == None: raise KeyError
			return render_template('single_item.html',
			                        z=zip,
			                        headers=headers,
			                        keys=keys,
			                        functions=functions,
			                        path=path_val,
			                        obj=obj)

		#if there are args, query object's db
		db, headers_null, keys_null, functions_null = query_dict[obj_id]
		t = db.query.filter_by(**queries)
		if t == None: raise KeyError
		t = t.first().models.all()

		db, headers, keys, functions = query_dict[path_val]
		return render_template('table.html',
									z=zip,
									keys=keys,
									functions=functions,
									path=path_val,
									headers=headers,
									t=t)
	except TemplateNotFound:
		abort(404)
	except KeyError:
		abort(404)



@app.route('/search/', methods=['GET'])
@app.route('/search', methods=['GET'])
def search_func():
	ordering, items = refine_search.optimized_search(request.args.get('q'))
	return render_template('search.html', 
									len=len,
									z=zip,
									query_dict = query_dict,
									ordering = ordering,
									items = items,
									DB_IDX=0,
									KEY_IDX=2,
									HEADER_IDX=1,
									FUNCTION_IDX=3)



# -------
#  about
# -------
@app.route('/about')
def about() :
	return render_template('about.html')


# -------
#  tests
# -------
@app.route('/tests')
def tests() :
	cmd = ["make","test"]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	out, err = p.communicate()
	with open('tests.tmp') as f:
		result = f.readlines()
	try :
		return render_template('tests.html', results=result)
	except TemplateNotFound:
		about(404)


# ------------------------------------
# tweetstats
# ------------------------------------
@app.route('/tweetstats/')
def tweet_stats() :
	return render_template('tweet_stats.html', t=tweet_coords)

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
