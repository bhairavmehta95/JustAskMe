# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = None

import time
import os
import random, string
from flask import *
from mysql_backend import *
import re

import socketio

application = Flask(__name__)
sio = socketio.Server(logger=True, async_mode=async_mode)
application.wsgi_app = socketio.Middleware(sio, application.wsgi_app)
application.config['SECRET_KEY'] = 'secret!'
application.secret_key = 'es2uD2da32h4fRV328u5eg7Tufhd2du'	#  TODO: make better

@application.route('/index')
@application.route('/')
def default():
  session['admins'] = []
  return render_template('start_page.html')


@application.route('/<room>')
def room(room):
    if (request.method == 'POST'):
        if not json.loads(request.data).get('is_in_use'):
            new_passw = ''.join(random.choice(string.ascii_lowercase) for i in range(6))#gen rand letters
            session[room] = new_passw     # New cookie
            add_admin(new_passw,room)     # Add a new admin to the admin table

    return render_template('questions.html')    

@application.route('/api/genAdminPw', methods=['POST'])
def gen_admin_pw():
    namespace = json.loads(request.data).get('namespace')
    namespace = re.sub(r'[\W_]+', '', namespace)

    if namespace_exists(namespace):
        url_new = '/' + namespace
        return redirect(url_for(url_new))

    new_passw = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    return json.dumps({
        'password':new_passw,
        'namespace':namespace
        })

@application.route('/api/addRow', methods = ['POST'])
def api_add_row():
    json_data = request.json
    namespace = json_data['namespace']
    question = json_data['question']

    add_question(question, namespace)
    
    return json.dumps({
        'status_code' : 200
    })

@application.route('/api/getAnsweredChron', methods=['POST'])
def api_answered_chron():
    json_data = request.json
    namespace = json_data['namespace']

    get_questions_sorted_answered(namespace)

    return json.dumps({
        'status_code' : 200
    })

@application.route('/api/addAdmin', methods = ['POST'])
def api_add_admin():
    namespace = json.loads(request.data).get('namespace')
    admin_pass = json.loads(request.data).get('password')

    add_admin(admin_pass, namespace)

    return json.dumps({
        'status_code' : 200
    })

@application.route('/api/getRowsChron', methods = ['POST'])
def api_get_rows_chron():
    json_data = request.json
    namespace = json_data['namespace']
    
    rows = get_questions_sorted_new_unanswered(namespace)
    unique_ids = []
    questions = []
    timestamps = []
    upvotes = []

    for val in rows:
        unique_ids.append(val[0])
        questions.append(val[1])
        upvotes.append(val[2])
        timestamps.append(val[3])
        
    return json.dumps({
        'unique_ids' : unique_ids,
        'questions' : questions,
        'timestamps' : timestamps,
        'upvotes' : upvotes
        })


@application.route('/api/getRowsTop', methods=['POST'])
def api_get_rows_top():
    json_data = request.json
    namespace = json_data['namespace']
    
    rows = get_questions_sorted_top_unanswered(namespace)
    questions = []
    timestamps = []
    upvotes = []
    unique_ids = []

    for val in rows:
        unique_ids.append(val[0])
        questions.append(val[1])
        upvotes.append(val[2])
        timestamps.append(val[3])

    return json.dumps({
        'unique_ids' : unique_ids,
        'questions' : questions,
        'timestamps' : timestamps,
        'upvotes' : upvotes
        })

@application.route('/api/addUpvote', methods=['POST'])
def api_add_upvote():
    json_data = request.json
    unique_id = json_data['unique_id']
    add_upvote = json_data['add_upvote']

    increment_upvotes_by_one(unique_id, add_upvote)

    return json.dumps({

        })

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
    unique_id = add_question(message['data'], message['room'])
    sio.emit('my response', {'data': message['data']}, room=message['room'],
             namespace='/')
    

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
