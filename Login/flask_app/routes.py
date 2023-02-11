# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()    

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
	return session['email'] if 'email' in session else 'Unknown'

@app.route('/login')
def login():
	return render_template('login.html', failed_attempts=0)

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
	print('I begin to process login')
	success = db.authenticate(form_fields['email'], form_fields['password'])

	if success['success'] == 1:
		session['email'] = form_fields['email']
		session.pop('attempt', default=None)
		x = random.choice(['I started university when I was a wee lad of 15 years.','I have a pet sparrow.','I write poetry.'])
		#return json.dumps(success)
		return redirect("/home")
	else:
		#return render_template('login.html', user=getUser(), failed_attempts=(form_fields['attempt']+1))
		if 'attempt' not in session:
			session['attempt'] = 1
		else:
			session['attempt'] += 1
		return render_template('login.html', user=getUser(), failed_attempts=session['attempt'])
		#return json.dumps(success)


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')

@socketio.on('left', namespace='/chat')
def left(message):
	emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
	leave_room('main')

@socketio.on('my event', namespace='/chat')
def handle_my_custom_event(message):
	send(message, json=True)
	print('message recieved')
	emit('status', {'msg': getUser() + ' has sent a message.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')

@socketio.on('json', namespace='/chat')
def handle_json(message):
	print("Message has been send")
	emit('status', {'msg': message[msg] + message['user'], 'style': 'width: 100%;color:blue;text-align: right'}, room='main')


# @socketio.on('my event', namespace='/chat')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))
# 	emit('status', {'msg': getUser() + ' has sent a chat', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')

# @socketio.on('json',  namespace='/chat')
# def handle_json(json):
#     send(json, json=True)

# @socketio.on('send_message', namespace='/chat')
# def send_message(message):
# 	if message['user'] == getUser():
# 		io.to('main').emit('status', {'msg': message + ' has left the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
# 	else:
# 		io.to('main').emit('status', {'msg': message + ' has left the room.', 'style': 'width: 100%;color:blue;text-align: left'}, room='main')
# 	#send(message)

# @socketio.on('message',  namespace='/chat')
# def handle_message(message):
# 	user = getUser()
# 	emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
    

	
# emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
	


#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	print(db.query('SELECT * FROM users'))
	x = random.choice(['I started university when I was a wee lad of 15 years.','I have a pet sparrow.','I write poetry.'])
	return render_template('home.html', user=getUser(), fun_fact = x)

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

@app.route('/sign')
def signup():
	return render_template('sign.html')


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
