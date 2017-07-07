# import os
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

user_states = {
    'john': False,
    'navin': False,
    'winnie': False,
    'sameer': False,
}

last_brewed_at = None


@app.route('/')
def index():
    return render_template('control.html')


if __name__ == '__main__':
    socketio.run(app)

# ================================================
# Socket IO communication logic
# ================================================


@socketio.on('new-connection')
def handle_new_connection():
    emit_state(broadcast=False)


# CONTRACT:
# data = { 'user': string, 'checked': boolean }
@socketio.on('change-state')
def handle_user_state_changed(data):
    user_states[data['user']] = data['checked']
    # Update state on all connected clients
    emit_state(broadcast=True)


@socketio.on('reset-state')
def handler_reset_states():
    for k in user_states:
        user_states[k] = False
    global last_brewed_at
    last_brewed_at = datetime.now()
    emit_state(broadcast=True)


def emit_state(broadcast=True):
    emit('state', get_user_states_payload(), broadcast=True)


# CONTRACT:
# returns an array of all user states, e.g.
# [ { user: 'john', checked: True }, ... ]
def get_user_states_payload():
    states = []
    for k, v in user_states.iteritems():
        states.append({'user': k, 'checked': v})
    return {
        'userStates': states,
        'lastBrewed': str(last_brewed_at)
    }
