from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Diccionario para almacenar los nombres de usuario asociados con sus conexiones
users = {}

@socketio.on('connect')
def handle_connect():
    # Asignar un nombre de usuario aleatorio al cliente conectado
    username = 'Usuario' + str(len(users) + 1)
    users[request.sid] = username
    emit('username', username)
    emit_users()

@socketio.on('disconnect')
def handle_disconnect():
    # Eliminar el nombre de usuario cuando el cliente se desconecta
    del users[request.sid]
    emit_users()

@socketio.on('message')
def handle_message(data):
    sender = users[request.sid]
    recipient = data['recipient']
    message = f"{sender} -> {recipient}: {data['message']}"
    emit('message', message, broadcast=True)

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username
    emit('username', username)
    emit_users()

def emit_users():
    user_list = [username for sid, username in users.items()]
    emit('users', user_list, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
