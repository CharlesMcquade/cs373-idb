from flask import render_template, redirect, abort
from jinja2 import TemplateNotFound
from app import app
import json

with open('dat/engines.json') as i : engine_dict = json.load(i)
with open('dat/makes.json') as i : makes_dict = json.load(i)
with open('dat/models.json') as i : models_dict = json.load(i)
# ---------
#  index
# ---------
@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html')


# ---------
#  models
# ---------
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

# ---------
#  makes
# ---------
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

# ---------
#  about
# ---------
@app.route('/about')
def about():
	return render_template('about.html')


