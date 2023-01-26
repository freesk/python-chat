from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time
import uuid

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

socketio = SocketIO(app, cors_allowed_origins="*")

# mimic database 
history = []

@socketio.on('connect')
def on_connect():
    emit('join', history)

OFFSET = 1000 * 60

# don't post join message more often than every minute
def is_message_new(message):
    now = time.time() * 1000
    return (now - OFFSET) < message['timestamp']

@socketio.on('join')
def on_join(data):
    print('data', str(data))
    print('data', str(history))
    if any(message['author'] == data['username'] and is_message_new(message) for message in history):
        return
    bot_message = { 
        'payload': data['username'] + ' has joined', 
        'id': str(uuid.uuid4()), 
        'bot': True, 
        'author': data['username'], 
        'timestamp': time.time() * 1000  
    }
    history.append(bot_message) 
    emit('message', bot_message, broadcast=True)

@socketio.on('message')
def on_message(data):
    data['timestamp'] = time.time() * 1000
    emit('message', data, broadcast=True)
    history.append(data) 

# port 5000 is not working on mac because of Air Play!
if __name__ == "__main__":
    app.run(port=4000)
