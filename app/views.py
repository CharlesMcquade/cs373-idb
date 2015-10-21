from flask import render_template, redirect
from app import app




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
def models():
	return render_template('model.html')


# ---------
#  makes
# ---------
@app.route('/makes')
def makes():
	return render_template('make.html')


# ---------
#  engines
# ---------
@app.route('/engines')
def engines():
	return render_template('engine.html')


# ---------
#  about
# ---------
@app.route('/about')
def about():
	return render_template('about.html')


# ---------
#  single_make
# ---------
@app.route('/single_make')
def single_make():
	return render_template('single_make.html')

# ---------
#  single_model
# ---------
@app.route('/single_model')
def single_model():
	return render_template('single_model.html')

# ---------
#  single_engine
# ---------
@app.route('/single_engine')
def single_engine():
	return render_template('single_engine.html')


# ---------
#  single_vehicle
# ---------
@app.route('/single_vehicle')
def single_vehicle():
	return render_template('single_vehicle.html')




