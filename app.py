from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    print(f"New connection: {session_id}")

@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    if session_id in users:
        del users[session_id]
    print(f"Disconnected: {session_id}")

@socketio.on('set_username')
def handle_set_username(username):
    session_id = request.sid
    users[session_id] = username
    print(f"User set: {username} with session ID: {session_id}")

@socketio.on('message')
def handle_message(msg):
    session_id = request.sid
    username = users.get(session_id, 'Anônimo')
    print(f"Message from {username}: {msg}")
    send({'user': username, 'msg': msg}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
