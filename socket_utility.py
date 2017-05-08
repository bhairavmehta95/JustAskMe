from flask import *
from mysql_backend import *
from flask_socketio import SocketIO, join_room, emit

application = Flask(__name__)
sio = SocketIO(application)
application.config['SECRET_KEY'] = 'es2uD2da32h4fRV328u5eg7Tufhd2du'
application.secret_key = 'es2uD2da32h4fRV328u5eg7Tufhd2du'

@sio.on('join', namespace='/')
def join(message):
    join_room(message['room'])
    emit('my response', {'data': 'Entered room: ' + message['room']},
             room=message['room'], namespace='/')


@sio.on('my room event', namespace='/')
def send_room_message(message):
    add_question(message['data'], message['room'])
    emit('my response', {'data': message['data']}, room=message['room'],
             namespace='/')

@sio.on('connect', namespace='/')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0}, namespace='/')