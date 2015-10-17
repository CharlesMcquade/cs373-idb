from flask import render_template, redirect
from app import app






@app.route('/index')
@app.route('/')
def index():
	user = {'nickname':'Joe'}
	return render_template('index.html',
				user=user)
