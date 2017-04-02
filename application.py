# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = None

import time
import os
import random, string
from flask import *
from mysql_backend import *

import socketio

sio = socketio.Server(logger=True, async_mode=async_mode)
application = Flask(__name__)
application.wsgi_app = socketio.Middleware(sio, application.wsgi_app)
application.config['SECRET_KEY'] = 'secret!'
application.secret_key = 'es2uD2da32h4fRV328u5eg7Tufhd2du'	#  TODO: make better

# @app.route('/')
#   def clickGo():
#     if (request.method == 'GET'):
#   return render_template('index.html')
# elif (request.method == 'POST'):
#       num_namespace = count_namespace("###get namespace from textbox###")
#       if (!num_namespace):
#         #Alert user that no such namespace exists, creating new one- JS/HTML in future
#         passw = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
#         session["###get namespace from textbox###"] = passw
#         # Add new row to namespaces table
#       else:
#         # Alert user that they are joining an existing page- might be a JS/HTML thing in future 
# 	# Check if user has cookie to be admin
#         # Else just enter as normal user
#         pass	# until code is written     
#       return redirect(url_for("###get namespace from textbox###"), code=307)


@application.route('/<room>')
def index(room):
    return render_template('index.html')


@application.route('/api/addRow', methods = ['POST'])
def api_add_row():
    json_data = request.json
    namespace = json_data['namespace']
    question = json_data['question']

    add_question(question, namespace)

@application.route('/api/getRowsChron', methods = ['POST'])
def api_get_rows_chron():
    json_data = request.json
    namespace = json_data['namespace']
    
    rows = get_questions_sorted_new_unanswered(namespace)
    questions = []
    timestamps = []
    upvotes = []

    print(rows)

    for val in rows:
        if not val[5]:
            questions.append(val[1])
            upvotes.append(val[2])
            timestamps.append(val[3])
            
    return json.dumps({
        'questions' : questions,
        'timestamps' : timestamps,
        'upvotes' : upvotes
        })


@application.route('/api/getRowsTop')
def api_get_rows_top():
    json_data = request.json
    namespace = json_data['namespace']
    
    rows = get_questions_sorted_top_unanswered(namespace)
    questions = []
    timestamps = []
    upvotes = []

    for val in rows:
        if not val['answered']:
            questions.append(val['string'])
            timestamps.append(val['posted_time'])
            upvotes.append(val['upvotes'])

    return json.dumps({
        'questions' : questions,
        'timestamps' : timestamps,
        'upvotes' : upvotes
        })

@application.route('/api/addUpvote')
def api_add_upvote():
    json_data = request.json
    unique_id = json_data['unique_id']

    increment_upvotes_by_one(unique_id)

@application.route('/api/sortChron', methods = ['POST'])
def sort_chronological():
    json_data = request.json
    namespace_value = request['namespace']
    order = get_questions_sorted_new_unanswered(namespace_value)
    return json.dumps({
        'questions' : order['string'],
        'timestamps' : order['posted_time'],
        'upvotes'  :order['upvotes']
        })

@application.route('/api/sortTop', methods = ['POST'])
def sort_top():
    json_data = request.json
    namespace_value = request['namespace']
    order = get_questions_sorted_top_unanswered(namespace_value)
    return json.dumps({
        'questions' : order['string'],
        'timestamps' : order['posted_time'],
        'upvotes' : order['upvotes']
        })


@sio.on('my event', namespace='/')
def test_message(sid, message):
    sio.emit('my response', {'data': message['data']}, room=sid,
             namespace='/')


@sio.on('my broadcast event', namespace='/')
def test_broadcast_message(sid, message):
    sio.emit('my response', {'data': message['data']}, namespace='/')


@sio.on('join', namespace='/')
def join(sid, message):
    sio.enter_room(sid, message['room'], namespace='/')
    sio.emit('my response', {'data': 'Entered room: ' + message['room']},
             room=sid, namespace='/')


@sio.on('leave', namespace='/')
def leave(sid, message):
    sio.leave_room(sid, message['room'], namespace='/')
    sio.emit('my response', {'data': 'Left room: ' + message['room']},
             room=sid, namespace='/')


@sio.on('close room', namespace='/')
def close(sid, message):
    sio.emit('my response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'], namespace='/')
    sio.close_room(message['room'], namespace='/')


@sio.on('my room event', namespace='/')
def send_room_message(sid, message):
    sio.emit('my response', {'data': message['data']}, room=message['room'],
             namespace='/')
    add_question(message['data'], message['room'])

@sio.on('disconnect request', namespace='/')
def disconnect_request(sid):
    sio.disconnect(sid, namespace='/')


@sio.on('connect', namespace='/')
def test_connect(sid, environ):
    sio.emit('my response', {'data': 'Connected', 'count': 0}, room=sid,
             namespace='/')


@sio.on('disconnect', namespace='/')
def test_disconnect(sid):
    print('Client disconnected')


if __name__ == '__main__':
    if sio.async_mode == 'threading':
        # deploy with Werkzeug
        application.run(threaded=True)
    elif sio.async_mode == 'eventlet':
        # deploy with eventlet
        import eventlet
        import eventlet.wsgi
        eventlet.wsgi.server(eventlet.listen(('', 5000)), application)
    elif sio.async_mode == 'gevent':
        # deploy with gevent
        from gevent import pywsgi
        try:
            from geventwebsocket.handler import WebSocketHandler
            websocket = True
        except ImportError:
            websocket = False
        if websocket:
            pywsgi.WSGIServer(('', 5000), application,
                              handler_class=WebSocketHandler).serve_forever()
        else:
            pywsgi.WSGIServer(('', 5000), application).serve_forever()
    elif sio.async_mode == 'gevent_uwsgi':
        print('Start the application through the uwsgi server. Example:')
        print('uwsgi --http :5000 --gevent 1000 --http-websockets --master '
              '--wsgi-file apppplication.py --callable app')
    else:
        print('Unknown async_mode: ' + sio.async_mode)