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
