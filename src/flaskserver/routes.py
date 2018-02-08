from app import app
from flask import request
from app import stuff

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/register',methods=['GET', 'POST'])
def register():
	global stuff
	stuff.append(request.form['ID'])
	print(stuff)
	return "Registered!"

@app.route('/list')
def list():
	global stuff
	resp = "<ul>"
	for reg in stuff:
		resp = resp + "<li>{}</li>".format(reg)
	return resp

