# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request
from .utils.database.database  import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
db = database()

@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x     = random.choice(['I can beat you in any arcade game','I have 5 siblings.','I love cooking.'])
	return render_template('home.html', fun_fact = x)

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)

@app.route('/projects')
def projects():
	return render_template('projects.html')

@app.route('/piano')
def piano():
	return render_template('piano.html')


@app.route('/processfeedback', methods = ['POST'])
def processfeedback():
	feedback = request.form
	if feedback.get("name") != None and feedback.get("email") != None and feedback.get("comment") != None:
		db.insertRows('feedback', ['comment_id', 'name', 'email', 'comment'], [['NULL', feedback.get('name'), feedback.get('email'), feedback.get('comment')]])
	dict_feedback = db.query('SELECT * FROM feedback')
	return render_template('processfeedback.html', val = dict_feedback)