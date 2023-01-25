from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time

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

@socketio.on('message')
def on_message(data):
    data['timestamp'] = time.time() * 1000
    emit('message', data, broadcast=True)
    history.append(data) 

if __name__ == "__main__":
    app.run()
