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

@socketio.on('disconnect')
def handle_disconnect():
    # Eliminar el nombre de usuario cuando el cliente se desconecta
    del users[request.sid]

@socketio.on('message')
def handle_message(data):
    username = users[request.sid]
    message = f"{username}: {data['message']}"
    emit('message', message, broadcast=True)

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username
    emit('username', username)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
