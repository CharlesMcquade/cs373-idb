from flask import render_template, redirect, abort, request, jsonify
from jinja2 import TemplateNotFound
from app import app
import json
import subprocess
from app import db
from models import Make, Model, Engine, Type

with open('dat/engines.json') as i : engine_dict = json.load(i)
with open('dat/makes.json') as i : makes_dict = json.load(i)
with open('dat/models.json') as i : models_dict = json.load(i)
with open('dat/types.json') as i : types_dict = json.load(i)
with open('dat/transmissions.json') as i : tranny_dict = json.load(i)

# -------
#  index
# -------
@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html')


# --------
#  models
# --------
@app.route('/models')
@app.route('/models/')
def models():
	return render_template('models.html', models=models_dict)

@app.route('/models/<make>/<model>')
def single_model(make, model):
	try :
		return render_template('single_model.html', make_name=make, model_name=model, model=models_dict[make][model])
	except TemplateNotFound:
		abort(404)

# -------
#  makes
# -------
@app.route('/makes')
@app.route('/makes/')
def makes():
	return render_template('makes.html', makes=makes_dict)

@app.route('/makes/<make_id>')
def single_make(make_id):
	try :
		return render_template('single_make.html', name=make_id, make=makes_dict[make_id])
	except TemplateNotFound:
		abort(404)

# ---------
#  engines
# ---------
@app.route('/engines')
@app.route('/engines/')
def engines():
	return render_template('engines.html', engines=engine_dict)



@app.route('/engines/<engine_id>')
def single_engine(engine_id):
	try :
		return render_template('single_engine.html', engine=engine_dict[engine_id])
	except TemplateNotFound:
		abort(404)


@app.route('/types/<type_id>')
def single_type(type_id):
	try :
		return render_template('single_type.html', name=type_id, type=types_dict[type_id])
	except TemplateNotFound:
		abort(404)

@app.route('/transmissions/<tran_id>')
def single_transmission(tran_id):
	try :
		return render_template('single_transmission.html', name=tran_id, tran=tranny_dict[tran_id])
	except TemplateNotFound:
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
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	out, err = p.communicate()
	return (out)

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
