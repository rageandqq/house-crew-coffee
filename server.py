import os
import pytz
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


# ================================================
# Flask and SocketIO setup
# ================================================

app = Flask(__name__)
socketio = SocketIO(app)


# ================================================
# Server setup and routing
# ================================================

@app.route('/')
def index():
    return render_template('control.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    socketio.run(app, port=port, host='0.0.0.0')

# ================================================
# State
# ================================================

user_states = {
    'john': False,
    'navin': False,
    'winnie': False,
    'sameer': False,
}

last_brewed_at = None


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
    last_brewed_at = datetime.now(pytz.timezone('US/Eastern'))
    emit_state(broadcast=True)
    emit('new-pot', broadcast=True, include_self=False)


def emit_state(broadcast=True):
    emit('state', get_user_states_payload(), broadcast=True)


# CONTRACT:
# returns a dict with array of all user states and last brewed time, e.g.
# {
#    'userStates': [ { user: 'john', checked: True }, ... ],
#    'lastBrewed': '2017-07-07 17:22:41...'
# }
def get_user_states_payload():
    states = []
    for k, v in user_states.iteritems():
        states.append({'user': k, 'checked': v})
    return {
        'userStates': states,
        'lastBrewed': str(last_brewed_at) if last_brewed_at else None
    }
